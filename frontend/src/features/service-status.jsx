'use client';
import { useEffect, useState } from 'react';

export default function ServiceStatus() {
  const [status, setStatus] = useState('Checking local services…');
  useEffect(() => {
    const controller = new AbortController();
    fetch('/api/v1/health', { signal:controller.signal }).then(async response => {
      const body = await response.json();
      setStatus(response.ok && body.database === 'connected' ? 'Backend and database connected.' : 'Database unavailable. Your information cannot be saved yet.');
    }).catch(error => { if (error.name !== 'AbortError') setStatus('Backend unavailable. Start the local API to continue.'); });
    return () => controller.abort();
  }, []);
  return <div className="notice"><p role="status">{status}</p><p>AI planning is not configured yet.</p></div>;
}
