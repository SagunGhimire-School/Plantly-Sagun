'use client';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({name:z.string().trim().min(1).max(100),area_m2:z.coerce.number().positive().max(1e9),region:z.string().trim().min(1).max(200)});

export default function EditPlot({plot}) {
  const [open,setOpen] = useState(false);
  const [error,setError] = useState('');
  const cache = useQueryClient();
  const {register,handleSubmit,formState:{isSubmitting,errors}} = useForm({resolver:zodResolver(schema),defaultValues:{name:plot.name,area_m2:plot.area_m2,region:plot.location.region}});
  async function save(values) {
    setError('');
    try { await api(`/plots/${plot.id}`,{method:'PATCH',body:JSON.stringify({...values,expected_revision:plot.revision})}); await cache.invalidateQueries({queryKey:['dashboard']}); setOpen(false); }
    catch (failure) { setError(failure.code === 'INPUT_REVISION_CONFLICT' ? 'This plot changed in another tab. Reload before editing again.' : failure.message); }
  }
  if (!open) return <button className="secondary" onClick={() => setOpen(true)}>Edit plot details</button>;
  return <form className="stack" onSubmit={handleSubmit(save)}>
    <div><label htmlFor={`name-${plot.id}`}>Plot name</label><input id={`name-${plot.id}`} required maxLength={100} {...register('name')} /></div>
    <div><label htmlFor={`area-${plot.id}`}>Area (m²)</label><input id={`area-${plot.id}`} required type="number" min="0.0001" max="1000000000" step="0.0001" {...register('area_m2')} /></div>
    <div><label htmlFor={`region-${plot.id}`}>Growing region</label><input id={`region-${plot.id}`} required maxLength={200} {...register('region')} /></div>
    {error && <p role="alert" className="error">{error}</p>}
    {Object.keys(errors).length > 0 && <p role="alert" className="error">Enter a plot name, positive area and growing region.</p>}
    <div className="actions"><button disabled={isSubmitting}>{isSubmitting ? 'Saving…' : 'Save plot details'}</button><button type="button" className="secondary" onClick={() => setOpen(false)}>Cancel</button></div>
  </form>;
}
