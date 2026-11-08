'use client';
import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import EditPlot from './edit-plot';

export default function Garden({plotId,seasonId}) {
  const params = new URLSearchParams();
  if (plotId) params.set('plot_id',plotId);
  if (seasonId) params.set('season_id',seasonId);
  const query = useQuery({queryKey:['dashboard',plotId,seasonId],queryFn:() => api(`/dashboard?${params}`)});
  if (query.isPending) return <p role="status">Loading your growing records…</p>;
  if (query.error) return <div role="alert"><p>{query.error.message}</p><button onClick={() => query.refetch()}>Try again</button><p><Link href="/login">Log in again</Link></p></div>;
  const data = query.data;
  return <>
    {!data.contexts.length ? <div className="panel"><h2>No plots saved yet.</h2><p>Start with a name, area and season. You can save a draft and return when you have more information.</p><Link className="button" href="/onboarding">Set up your first plot</Link></div> : <>
      {data.contexts.map(context => <article className="panel" key={context.id}><p className="eyebrow">SAVED GROWING RECORD</p><h2><Link href={`/dashboard?plot_id=${context.plot.id}&season_id=${context.season.id}`}>{context.plot.name}</Link></h2>
        <dl><dt>Season</dt><dd>{context.season.label} · {context.season.year}</dd><dt>Area</dt><dd>{Number(context.plot.area_m2)} m²</dd><dt>Region</dt><dd>{context.plot.location.region}</dd><dt>Crop goals</dt><dd>{context.inputs.crop_goals || 'Unknown'}</dd><dt>Crop history</dt><dd>{context.inputs.crop_history || 'Unknown'}</dd><dt>Soil pH</dt><dd>{context.inputs.soil_observation.ph == null ? 'Unknown — no measurement entered' : `${context.inputs.soil_observation.ph} (user-reported, ${context.inputs.soil_observation.observed_on})`}</dd><dt>Budget</dt><dd>{context.budget_amount == null ? 'Unknown' : `${context.budget_amount} ${context.currency}`}</dd></dl>
        <p className="muted">These are your entered facts, not a generated plan.</p>
        <EditPlot key={`${context.plot.id}-${context.plot.revision}`} plot={context.plot} />
      </article>)}
      <div className="actions"><Link className="button" href="/onboarding">Add another plot</Link>{(plotId || seasonId) && <Link href="/dashboard">View all plots</Link>}</div>
    </>}
    <section className="notice"><h2>Planning availability</h2><p>{data.planning.message}.</p><p>Scientific recommendations await review. Live weather and product prices are unavailable. No costs or savings have been calculated.</p><button disabled>Generate a plan</button></section>
  </>;
}
