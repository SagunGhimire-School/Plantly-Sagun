'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

const schema = z.object({email:z.email('Enter a valid email address.').max(254),password:z.string().min(12,'Use at least 12 characters.').max(128,'Use at most 128 characters.')});

export default function AuthForm({signup = false}) {
  const router = useRouter();
  const cache = useQueryClient();
  const [error,setError] = useState('');
  const {register,handleSubmit,formState:{errors,isSubmitting}} = useForm({resolver:zodResolver(schema)});
  async function submit(values) {
    setError('');
    try { await api(signup ? '/auth/signup' : '/auth/login',{method:'POST',body:JSON.stringify(values)}); cache.clear(); router.replace('/dashboard'); router.refresh(); }
    catch (failure) { setError(failure.message); }
  }
  return <section className="narrow"><p className="eyebrow">YOUR PLANTLY ACCOUNT</p><h1>{signup ? 'Start your garden record.' : 'Welcome back.'}</h1>
    <p>Local preview accounts are temporary. Email verification and password recovery are not available. Retention terms are not yet set.</p>
    <form className="stack" onSubmit={handleSubmit(submit)} noValidate>
      <div><label htmlFor="email">Email</label><input id="email" type="email" autoComplete="email" {...register('email')} aria-invalid={!!errors.email} aria-describedby={errors.email ? 'email-error' : undefined}/>{errors.email && <p id="email-error" className="error">{errors.email.message}</p>}</div>
      <div><label htmlFor="password">Password</label><input id="password" type="password" autoComplete={signup ? 'new-password' : 'current-password'} {...register('password')} aria-invalid={!!errors.password} aria-describedby="password-help"/><p id="password-help" className={errors.password ? 'field-help error' : 'field-help muted'}>{errors.password?.message || '12–128 characters.'}</p></div>
      {error && <p role="alert" className="error">{error}</p>}
      <div><button disabled={isSubmitting}>{isSubmitting ? 'Please wait…' : signup ? 'Create account' : 'Log in'}</button></div>
    </form>
    <p className="panel">{signup ? 'Already have an account? ' : 'New to Plantly? '}<Link href={signup ? '/login' : '/signup'}>{signup ? 'Log in' : 'Create an account'}</Link></p>
  </section>;
}
