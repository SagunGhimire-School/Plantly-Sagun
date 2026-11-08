'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

export default function Logout() {
  const [error,setError] = useState('');
  const [pending,setPending] = useState(false);
  const router = useRouter();
  const cache = useQueryClient();
  async function logout() {
    setPending(true); setError('');
    try { await api('/auth/logout',{method:'POST'}); cache.clear(); router.replace('/login'); router.refresh(); }
    catch (failure) { setError(failure.message); setPending(false); }
  }
  return <div><button className="secondary" onClick={logout} disabled={pending}>{pending ? 'Logging out…' : 'Log out'}</button>{error && <p role="alert" className="error">{error}</p>}</div>;
}
