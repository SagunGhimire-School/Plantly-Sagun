"""Opaque database sessions and same-origin CSRF protection."""

import hashlib
import hmac
import secrets
import threading
import time
import uuid
from collections import OrderedDict, deque
from datetime import UTC, datetime, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import DateTime, ForeignKey, String, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.config import settings
from app.db import Base, get_db

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
hasher = PasswordHasher()
DUMMY_HASH = hasher.hash(secrets.token_urlsafe(32))
CHALLENGE_KEY = secrets.token_bytes(32)
CHALLENGE_COOKIE = (
    "plantly_preauth_dev" if settings.environment == "local" else "__Host-plantly_preauth"
)


def now():
    return datetime.now(UTC)


def digest(token):
    return hashlib.sha256(token.encode()).hexdigest()


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email_normalized: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    disabled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class UserSession(Base):
    __tablename__ = "user_sessions"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    csrf_token: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=12, max_length=128)


def check_origin(request: Request):
    if (
        request.headers.get("origin") != settings.origin
        or request.headers.get("sec-fetch-site") == "cross-site"
    ):
        raise HTTPException(403, "ORIGIN_NOT_ALLOWED")


def set_cookie(response, name, value, max_age):
    response.set_cookie(
        name,
        value,
        max_age=max_age,
        httponly=True,
        secure=settings.environment != "local",
        samesite="lax",
        path="/",
    )


def active_session(request: Request, db: Session):
    token = request.cookies.get(settings.cookie_name, "")
    if not token or len(token) > 128:
        return None
    session = db.scalar(
        select(UserSession)
        .join(User)
        .where(
            UserSession.token_hash == digest(token),
            UserSession.revoked_at.is_(None),
            UserSession.expires_at > now(),
            UserSession.last_seen_at > now() - timedelta(hours=12),
            User.disabled_at.is_(None),
        )
    )
    return session


def require_session(request: Request, db: Session = Depends(get_db)):
    session = active_session(request, db)
    if session is None:
        raise HTTPException(401, "SIGN_IN_REQUIRED")
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        check_origin(request)
        if not hmac.compare_digest(request.headers.get("x-csrf-token", ""), session.csrf_token):
            raise HTTPException(403, "INVALID_CSRF_TOKEN")
        session.last_seen_at = now()
    return session


@router.get("/csrf")
def csrf(request: Request, response: Response, db: Session = Depends(get_db)):
    session = active_session(request, db)
    if session:
        return {"csrf_token": session.csrf_token}
    token = f"{int(time.time())}.{secrets.token_urlsafe(32)}"
    signature = hmac.new(CHALLENGE_KEY, token.encode(), hashlib.sha256).hexdigest()
    challenge = f"{token}.{signature}"
    set_cookie(response, CHALLENGE_COOKIE, challenge, 600)
    return {"csrf_token": challenge}


def check_challenge(request):
    check_origin(request)
    challenge = request.headers.get("x-csrf-token", "")
    if (
        not challenge
        or len(challenge) > 256
        or not hmac.compare_digest(challenge, request.cookies.get(CHALLENGE_COOKIE, ""))
    ):
        raise HTTPException(403, "INVALID_CSRF_TOKEN")
    try:
        timestamp, nonce, signature = challenge.split(".")
        age = time.time() - int(timestamp)
    except ValueError:
        raise HTTPException(403, "INVALID_CSRF_TOKEN") from None
    expected = hmac.new(CHALLENGE_KEY, f"{timestamp}.{nonce}".encode(), hashlib.sha256).hexdigest()
    if not 0 <= age <= 600 or not hmac.compare_digest(signature, expected):
        raise HTTPException(403, "INVALID_CSRF_TOKEN")


# ponytail: per-process limiter for local development; shared ingress limits are a G-020 gate.
attempts = OrderedDict()
attempt_lock = threading.Lock()


def rate_limit(request):
    key = request.client.host if request.client else "unknown"
    with attempt_lock:
        current = time.monotonic()
        bucket = attempts.setdefault(key, deque())
        while bucket and bucket[0] < current - 60:
            bucket.popleft()
        if len(bucket) >= 20:
            raise HTTPException(429, "TOO_MANY_ATTEMPTS")
        bucket.append(current)
        attempts.move_to_end(key)
        while len(attempts) > 10000:
            attempts.popitem(last=False)


def issue_session(user, request, response, db):
    old = active_session(request, db)
    if old:
        old.revoked_at = now()
    token = secrets.token_urlsafe(32)
    session = UserSession(
        user_id=user.id,
        token_hash=digest(token),
        csrf_token=secrets.token_urlsafe(32),
        expires_at=now() + timedelta(days=7),
    )
    db.add(session)
    db.commit()
    set_cookie(response, settings.cookie_name, token, 7 * 86400)
    response.delete_cookie(
        CHALLENGE_COOKIE,
        path="/",
        secure=settings.environment != "local",
        httponly=True,
        samesite="lax",
    )
    return {"id": str(user.id), "email": user.email_normalized}


@router.post("/signup", status_code=201)
def signup(body: Credentials, request: Request, response: Response, db: Session = Depends(get_db)):
    rate_limit(request)
    check_challenge(request)
    user = User(
        email_normalized=str(body.email).casefold(), password_hash=hasher.hash(body.password)
    )
    db.add(user)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "ACCOUNT_UNAVAILABLE") from None
    return issue_session(user, request, response, db)


@router.post("/login")
def login(body: Credentials, request: Request, response: Response, db: Session = Depends(get_db)):
    rate_limit(request)
    check_challenge(request)
    user = db.scalar(select(User).where(User.email_normalized == str(body.email).casefold()))
    try:
        hasher.verify(user.password_hash if user else DUMMY_HASH, body.password)
    except (VerificationError, InvalidHashError):
        raise HTTPException(401, "INVALID_CREDENTIALS") from None
    if not user or user.disabled_at:
        raise HTTPException(401, "INVALID_CREDENTIALS")
    if hasher.check_needs_rehash(user.password_hash):
        user.password_hash = hasher.hash(body.password)
    return issue_session(user, request, response, db)


@router.get("/me")
def me(session: UserSession = Depends(require_session), db: Session = Depends(get_db)):
    user = db.get(User, session.user_id)
    return {"id": str(user.id), "email": user.email_normalized}


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    session: UserSession = Depends(require_session),
    db: Session = Depends(get_db),
):
    session.revoked_at = now()
    db.commit()
    response.delete_cookie(
        settings.cookie_name,
        path="/",
        secure=settings.environment != "local",
        httponly=True,
        samesite="lax",
    )


@router.delete("/me", status_code=204)
def delete_account(
    response: Response,
    session: UserSession = Depends(require_session),
    db: Session = Depends(get_db),
):
    db.delete(db.get(User, session.user_id))
    db.commit()
    response.delete_cookie(
        settings.cookie_name,
        path="/",
        secure=settings.environment != "local",
        httponly=True,
        samesite="lax",
    )
