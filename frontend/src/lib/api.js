export async function api(path, options = {}) {
  const headers = {'Content-Type':'application/json', ...options.headers};
  if (options.method && !['GET','HEAD'].includes(options.method)) {
    const challenge = await api('/auth/csrf');
    headers['X-CSRF-Token'] = challenge.csrf_token;
  }
  let response;
  try { response = await fetch(`/api/v1${path}`, {...options, headers, credentials:'same-origin', cache:'no-store'}); }
  catch { throw new Error('The server is unavailable. Your entries have been kept on this page.'); }
  let body = null;
  if (response.status !== 204) { try { body = await response.json(); } catch { /* Non-JSON proxy failure. */ } }
  if (!response.ok) {
    const error = new Error(body?.error?.message || 'The server is unavailable. Please try again.');
    error.status = response.status;
    error.code = body?.error?.code;
    error.fields = body?.error?.fields || {};
    throw error;
  }
  return body;
}
