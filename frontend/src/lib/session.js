import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export async function currentUser() {
  const jar = await cookies();
  const name = process.env.APP_ENV && process.env.APP_ENV !== 'local' ? '__Host-plantly_session' : 'plantly_session_dev';
  const session = jar.get(name);
  if (!session) redirect('/login');
  let response;
  try {
    response = await fetch(`${process.env.INTERNAL_API_BASE_URL || 'http://127.0.0.1:8000'}/api/v1/auth/me`, {
      headers:{Cookie:`${name}=${session.value}`}, cache:'no-store', signal:AbortSignal.timeout(5000),
    });
  } catch { return null; }
  if (response.status === 401) redirect('/login');
  return response.ok ? response.json() : null;
}
