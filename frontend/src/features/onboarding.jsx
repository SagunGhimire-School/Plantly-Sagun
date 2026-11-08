'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { api } from '../lib/api';

const number = (schema) => z.preprocess(value => value === '' || value == null ? null : Number(value), schema.nullable());
const text = (max) => z.preprocess(value => value === '' || value == null ? null : value, z.string().trim().max(max).nullable());
const schema = z.object({
  season_id:text(36),
  plot_name:text(100), area_m2:number(z.number().positive().max(1e9)), region:text(200),
  season_label:text(100), year:number(z.number().int().min(1900).max(2200)),
  start_date:text(10), end_date:text(10), crop_goals:text(2000), crop_history:text(2000),
  soil_ph:number(z.number().min(0).max(14)), soil_observed_on:text(10), soil_method:text(200), soil_laboratory:text(200),
  resources:text(2000), budget_amount:number(z.number().min(0).max(1e9)), currency:text(3),
});
const labels = {plot_name:'Plot name',area_m2:'Area (m²)',region:'Growing region',season_label:'Season name',year:'Season year',start_date:'Season start (optional)',end_date:'Season end (optional)',crop_goals:'What would you like to grow? (optional)',crop_history:'Previous crops and issues (optional)',soil_ph:'Soil pH (optional)',soil_observed_on:'Soil observation date',soil_method:'Test method (optional)',soil_laboratory:'Laboratory (optional)',resources:'Resources and growing goals (optional)',budget_amount:'Budget amount (optional)',currency:'Currency code (for example USD)'};
const steps = [ ['plot_name','area_m2','region','season_label','year','start_date','end_date'], ['crop_goals','crop_history','soil_ph','soil_observed_on','soil_method','soil_laboratory','resources','budget_amount','currency'] ];

function DraftForm({draft}) {
  const router = useRouter();
  const cache = useQueryClient();
  const seasons = useQuery({queryKey:['seasons'],queryFn:() => api('/seasons')});
  const [revision,setRevision] = useState(draft.revision);
  const [startNew,setStartNew] = useState(draft.status === 'completed');
  const [step,setStep] = useState(draft.status === 'completed' ? 1 : draft.step);
  const [message,setMessage] = useState('');
  const [failure,setFailure] = useState(null);
  const [pending,setPending] = useState(false);
  const defaults = Object.fromEntries(Object.entries(draft.draft_data).map(([k,v]) => [k,draft.status === 'completed' ? '' : v ?? '']));
  const {register,handleSubmit,getValues,setError,formState:{errors,isDirty},reset} = useForm({resolver:zodResolver(schema),defaultValues:defaults,shouldUnregister:false});

  async function save(values,nextStep = step,finish = false) {
    setPending(true); setFailure(null); setMessage('');
    try {
      const saved = await api('/onboarding/draft',{method:'PUT',body:JSON.stringify({expected_revision:revision,step:nextStep,draft_data:values,start_new:startNew})});
      setStartNew(false);
      setRevision(saved.revision); setStep(nextStep); reset(Object.fromEntries(Object.entries(saved.draft_data).map(([k,v]) => [k,v ?? ''])));
      cache.setQueryData(['draft'],saved); setMessage('Draft saved. You can return to it later.');
      if (finish) {
        const ids = await api('/onboarding/complete',{method:'POST',body:JSON.stringify({expected_revision:saved.revision})});
        await cache.invalidateQueries({queryKey:['dashboard']});
        await cache.invalidateQueries({queryKey:['seasons']});
        cache.removeQueries({queryKey:['draft']});
        router.push(`/dashboard?plot_id=${ids.plot_id}&season_id=${ids.season_id}`);
      }
    } catch (error) {
      setFailure(error);
      for (const [key,value] of Object.entries(error.fields || {})) {
        const field = key.replace('draft_data.','');
        if (labels[field]) setError(field,{message:value});
      }
    } finally { setPending(false); }
  }

  function field(name) {
    const numeric = ['area_m2','year','soil_ph','budget_amount'].includes(name);
    const type = name.includes('date') || name === 'soil_observed_on' ? 'date' : numeric ? 'number' : 'text';
    const props = {id:name,...register(name),'aria-invalid':!!errors[name],'aria-describedby':errors[name] ? `${name}-error` : undefined};
    return <div key={name}><label htmlFor={name}>{labels[name]}</label>{['crop_goals','crop_history','resources'].includes(name) ? <textarea {...props}/> : <input {...props} type={type} step={name === 'year' ? 1 : 'any'} />}{errors[name] && <p className="error" id={`${name}-error`}>{errors[name].message}</p>}</div>;
  }

  return <section className="narrow"><p className="eyebrow">STEP {step} OF 3 · {isDirty ? 'UNSAVED CHANGES' : 'GARDEN SETUP'}</p><h1>{['Your plot and season.','What you know so far.','Review your growing record.'][step-1]}</h1>
    <p>{step === 1 ? 'Name your plot and growing season. Use square metres for area; you can save an incomplete draft.' : step === 2 ? 'Leave anything you don’t know blank. Entered observations are user-reported, even when copied from a lab report.' : 'Check your facts before saving the plot. This saves your information; AI planning is not configured yet.'}</p>
    <form className="stack" onSubmit={handleSubmit(values => save(values))} noValidate>
      {step === 1 && <div><label htmlFor="season_id">Use an existing season (optional)</label><select id="season_id" {...register('season_id')}><option value="">Create a new season below</option>{seasons.data?.map(season => <option key={season.id} value={season.id}>{season.label} · {season.year}</option>)}</select><p className="field-help muted">If you choose an existing season, its saved name and dates will be used.</p>{seasons.error && <p className="error">Existing seasons could not be loaded. <button type="button" className="secondary" onClick={() => seasons.refetch()}>Retry</button></p>}</div>}
      {step === 3 && getValues('season_id') && <p>Using saved season: {seasons.data?.find(season => season.id === getValues('season_id'))?.label || 'Selected season'}. Its saved dates apply.</p>}
      {step < 3 ? steps[step-1].map(field) : <dl>{Object.entries(labels).filter(([key]) => !getValues('season_id') || !['season_label','year','start_date','end_date'].includes(key)).map(([key,label]) => <div className="review-row" key={key}><dt>{label}</dt><dd>{getValues(key) === '' || getValues(key) == null ? 'Unknown' : String(getValues(key))}</dd></div>)}</dl>}
      {failure && <div role="alert" className="error"><p>{failure.code === 'INPUT_REVISION_CONFLICT' ? 'This draft changed in another tab. Your entries remain here. Copy any changes before reloading the saved draft.' : failure.message}</p>{Object.entries(failure.fields || {}).filter(([key]) => !labels[key.replace('draft_data.','')]).map(([key,value]) => <p key={key}>{value}</p>)}{failure.code === 'INPUT_REVISION_CONFLICT' && <button type="button" className="secondary" onClick={() => window.location.reload()}>Reload saved draft</button>}</div>}
      <p role="status">{message}</p>
      <div className="actions">
        <button type="submit" className="secondary" disabled={pending}>Save draft</button>
        {step > 1 && <button type="button" className="secondary" disabled={pending} onClick={() => {setStep(step-1); setMessage('');}}>Back</button>}
        {step < 3 ? <button type="button" disabled={pending} onClick={handleSubmit(values => save(values,step+1))}>{pending ? 'Saving…' : 'Save and continue'}</button> : <button type="button" disabled={pending} onClick={handleSubmit(values => save(values,3,true))}>{pending ? 'Saving…' : 'Save plot and season'}</button>}
      </div>
    </form>
  </section>;
}

export default function Onboarding() {
  const query = useQuery({queryKey:['draft'],queryFn:() => api('/onboarding/draft')});
  if (query.isPending) return <p role="status">Loading your saved draft…</p>;
  if (query.error) return <div role="alert"><h1>Your draft could not be loaded.</h1><p>{query.error.message}</p><button onClick={() => query.refetch()}>Try again</button></div>;
  return <DraftForm draft={query.data} />;
}
