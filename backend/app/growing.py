"""Owner-scoped growing records and revision-safe, resumable intake."""

import uuid
from datetime import date, datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    select,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.ai import GeminiAdapter
from app.auth import User, UserSession, now, require_session
from app.db import Base, get_db

router = APIRouter(prefix="/api/v1", tags=["growing"])


class Plot(Base):
    __tablename__ = "plots"
    __table_args__ = (
        CheckConstraint("area_m2 > 0", name="plot_positive_area"),
        UniqueConstraint("id", "user_id"),
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(100))
    area_m2: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    location_data: Mapped[dict] = mapped_column(JSONB)
    revision: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Season(Base):
    __tablename__ = "seasons"
    __table_args__ = (
        UniqueConstraint("id", "user_id"),
        CheckConstraint(
            "end_date IS NULL OR start_date IS NULL OR end_date >= start_date",
            name="season_date_order",
        ),
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    label: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="planned")


class PlotSeason(Base):
    __tablename__ = "plot_seasons"
    __table_args__ = (
        UniqueConstraint("plot_id", "season_id"),
        ForeignKeyConstraint(
            ["plot_id", "user_id"], ["plots.id", "plots.user_id"], ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["season_id", "user_id"], ["seasons.id", "seasons.user_id"], ondelete="CASCADE"
        ),
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    plot_id: Mapped[uuid.UUID] = mapped_column(index=True)
    season_id: Mapped[uuid.UUID] = mapped_column(index=True)
    goals: Mapped[dict] = mapped_column(JSONB)
    budget_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    currency: Mapped[str | None] = mapped_column(String(3))
    revision: Mapped[int] = mapped_column(default=1)


class Draft(Base):
    __tablename__ = "onboarding_drafts"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    draft_data: Mapped[dict] = mapped_column(JSONB)
    revision: Mapped[int] = mapped_column(default=1)
    schema_version: Mapped[int] = mapped_column(default=1)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    step: Mapped[int] = mapped_column(default=1)
    completed_ids: Mapped[dict | None] = mapped_column(JSONB)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class InputData(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    season_id: uuid.UUID | None = None
    plot_name: str | None = Field(default=None, max_length=100)
    area_m2: Decimal | None = Field(default=None, gt=0, le=1000000000, decimal_places=4)
    region: str | None = Field(default=None, max_length=200)
    season_label: str | None = Field(default=None, max_length=100)
    year: int | None = Field(default=None, ge=1900, le=2200)
    start_date: date | None = None
    end_date: date | None = None
    crop_goals: str | None = Field(default=None, max_length=2000)
    crop_history: str | None = Field(default=None, max_length=2000)
    soil_ph: Decimal | None = Field(default=None, ge=0, le=14, decimal_places=2)
    soil_observed_on: date | None = None
    soil_method: str | None = Field(default=None, max_length=200)
    soil_laboratory: str | None = Field(default=None, max_length=200)
    resources: str | None = Field(default=None, max_length=2000)
    budget_amount: Decimal | None = Field(default=None, ge=0, le=1000000000, decimal_places=2)
    currency: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")

    @model_validator(mode="after")
    def consistent(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("Season end must be on or after its start.")
        if self.soil_ph is not None and self.soil_observed_on is None:
            raise ValueError("Add the observation date for the entered soil pH.")
        if self.soil_observed_on and self.soil_observed_on > date.today():
            raise ValueError("Soil observation date cannot be in the future.")
        if self.budget_amount is not None and not self.currency:
            raise ValueError("Add a currency code for your budget.")
        return self


class SaveDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start_new: bool = False
    expected_revision: int = Field(ge=0)
    step: int = Field(ge=1, le=3)
    draft_data: InputData


class CompleteDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_revision: int = Field(ge=1)


def owner_lock(db, user_id):
    # Serialize this grower's draft creation/completion; unrelated growers remain independent.
    db.scalar(select(User).where(User.id == user_id).with_for_update())


def draft_view(draft):
    if draft is None:
        return {
            "revision": 0,
            "status": "draft",
            "step": 1,
            "draft_data": InputData().model_dump(mode="json"),
        }
    return {
        "revision": draft.revision,
        "status": draft.status,
        "step": draft.step,
        "draft_data": draft.draft_data,
        "completed_ids": draft.completed_ids,
    }


@router.get("/onboarding/draft")
def get_draft(session: UserSession = Depends(require_session), db: Session = Depends(get_db)):
    return draft_view(db.scalar(select(Draft).where(Draft.user_id == session.user_id)))


@router.put("/onboarding/draft")
def save_draft(
    body: SaveDraft, session: UserSession = Depends(require_session), db: Session = Depends(get_db)
):
    owner_lock(db, session.user_id)
    draft = db.scalar(select(Draft).where(Draft.user_id == session.user_id))
    if body.expected_revision != (draft.revision if draft else 0):
        raise HTTPException(409, "INPUT_REVISION_CONFLICT")
    if draft and draft.status == "completed" and not body.start_new:
        # A repeated browser submission after a lost completion response must not create
        # another plot. Only the explicit add-another-plot flow resets a completed draft.
        if draft.draft_data == body.draft_data.model_dump(mode="json"):
            return draft_view(draft)
        raise HTTPException(409, "DRAFT_ALREADY_COMPLETED")
    if draft is None:
        draft = Draft(user_id=session.user_id, revision=0)
        db.add(draft)
    draft.draft_data = body.draft_data.model_dump(mode="json")
    draft.revision += 1
    draft.step, draft.status, draft.completed_ids = body.step, "draft", None
    draft.updated_at = now()
    db.commit()
    return draft_view(draft)


@router.post("/onboarding/complete")
def complete(
    body: CompleteDraft,
    session: UserSession = Depends(require_session),
    db: Session = Depends(get_db),
):
    owner_lock(db, session.user_id)
    draft = db.scalar(select(Draft).where(Draft.user_id == session.user_id))
    if draft is None:
        raise HTTPException(404, "DRAFT_NOT_FOUND")
    if body.expected_revision != draft.revision:
        raise HTTPException(409, "INPUT_REVISION_CONFLICT")
    if draft.status == "completed":
        return draft.completed_ids
    data = InputData.model_validate(draft.draft_data)
    if not all([data.plot_name, data.area_m2, data.region]) or (
        not data.season_id and not all([data.season_label, data.year])
    ):
        raise HTTPException(422, "PLOT_AREA_REGION_AND_SEASON_REQUIRED")
    if data.season_id:
        season = db.scalar(
            select(Season).where(Season.id == data.season_id, Season.user_id == session.user_id)
        )
        if not season:
            raise HTTPException(404, "SEASON_NOT_FOUND")
    else:
        season = Season(
            user_id=session.user_id,
            label=data.season_label,
            year=data.year,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        db.add(season)
    plot = Plot(
        user_id=session.user_id,
        name=data.plot_name,
        area_m2=data.area_m2,
        location_data={"region": data.region, "source_type": "user_reported"},
    )
    db.add(plot)
    db.flush()
    context = PlotSeason(
        user_id=session.user_id,
        plot_id=plot.id,
        season_id=season.id,
        goals={
            "crop_goals": data.crop_goals,
            "crop_history": data.crop_history,
            "resources": data.resources,
            "soil_observation": {
                "ph": str(data.soil_ph) if data.soil_ph is not None else None,
                "unit": "pH",
                "observed_on": data.soil_observed_on.isoformat() if data.soil_observed_on else None,
                "method": data.soil_method,
                "laboratory": data.soil_laboratory,
                "source_type": "user_reported" if data.soil_ph is not None else "unknown",
                "scientifically_verified": False,
            },
        },
        budget_amount=data.budget_amount,
        currency=data.currency,
    )
    db.add(context)
    db.flush()
    draft.status = "completed"
    draft.completed_ids = {
        "plot_id": str(plot.id),
        "season_id": str(season.id),
        "plot_season_id": str(context.id),
    }
    db.commit()
    return draft.completed_ids


def plot_view(plot):
    return {
        "id": str(plot.id),
        "name": plot.name,
        "area_m2": str(plot.area_m2),
        "location": plot.location_data,
        "revision": plot.revision,
    }


def season_view(season):
    return {
        "id": str(season.id),
        "label": season.label,
        "year": season.year,
        "start_date": season.start_date,
        "end_date": season.end_date,
    }


class UpdatePlot(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    expected_revision: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=100)
    area_m2: Decimal = Field(gt=0, le=1000000000, decimal_places=4)
    region: str = Field(min_length=1, max_length=200)


@router.patch("/plots/{plot_id}")
def update_plot(
    plot_id: uuid.UUID,
    body: UpdatePlot,
    session: UserSession = Depends(require_session),
    db: Session = Depends(get_db),
):
    plot = db.scalar(
        select(Plot).where(Plot.id == plot_id, Plot.user_id == session.user_id).with_for_update()
    )
    if not plot:
        raise HTTPException(404, "PLOT_NOT_FOUND")
    if plot.revision != body.expected_revision:
        raise HTTPException(409, "INPUT_REVISION_CONFLICT")
    plot.name, plot.area_m2 = body.name, body.area_m2
    plot.location_data = {"region": body.region, "source_type": "user_reported"}
    plot.revision += 1
    plot.updated_at = now()
    db.commit()
    return plot_view(plot)


@router.get("/plots")
def plots(session: UserSession = Depends(require_session), db: Session = Depends(get_db)):
    return [
        plot_view(p)
        for p in db.scalars(
            select(Plot).where(Plot.user_id == session.user_id).order_by(Plot.created_at).limit(100)
        )
    ]


@router.get("/plots/{plot_id}")
def get_plot(
    plot_id: uuid.UUID,
    session: UserSession = Depends(require_session),
    db: Session = Depends(get_db),
):
    plot = db.scalar(select(Plot).where(Plot.id == plot_id, Plot.user_id == session.user_id))
    if not plot:
        raise HTTPException(404, "PLOT_NOT_FOUND")
    return plot_view(plot)


@router.get("/seasons")
def seasons(session: UserSession = Depends(require_session), db: Session = Depends(get_db)):
    return [
        season_view(s)
        for s in db.scalars(
            select(Season)
            .where(Season.user_id == session.user_id)
            .order_by(Season.year.desc(), Season.id)
            .limit(100)
        )
    ]


@router.get("/dashboard")
def dashboard(
    plot_id: uuid.UUID | None = None,
    season_id: uuid.UUID | None = None,
    session: UserSession = Depends(require_session),
    db: Session = Depends(get_db),
):
    query = select(PlotSeason).where(PlotSeason.user_id == session.user_id)
    if plot_id:
        query = query.where(PlotSeason.plot_id == plot_id)
    if season_id:
        query = query.where(PlotSeason.season_id == season_id)
    contexts = db.scalars(query.order_by(PlotSeason.id).limit(100)).all()
    if (plot_id or season_id) and not contexts:
        raise HTTPException(404, "GROWING_CONTEXT_NOT_FOUND")
    return {
        "contexts": [
            {
                "id": str(c.id),
                "plot": plot_view(db.get(Plot, c.plot_id)),
                "season": season_view(db.get(Season, c.season_id)),
                "inputs": c.goals,
                "budget_amount": str(c.budget_amount) if c.budget_amount is not None else None,
                "currency": c.currency,
            }
            for c in contexts
        ],
        "plan": None,
        "planning": GeminiAdapter().status(),
        "weather": {"status": "unavailable"},
        "prices": {"status": "unavailable"},
    }


@router.post("/plots/{plot_id}/plan-generations")
def planning_unavailable(
    plot_id: uuid.UUID,
    session: UserSession = Depends(require_session),
    db: Session = Depends(get_db),
):
    get_plot(plot_id, session, db)
    raise HTTPException(503, "AI_PLANNING_NOT_CONFIGURED")
