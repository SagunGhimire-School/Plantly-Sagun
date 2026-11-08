import test from 'node:test';
import assert from 'node:assert/strict';
import config from '../../next.config.mjs';

test('API uses the same-origin backend proxy', async () => {
  const [rule] = await config.rewrites();
  assert.equal(rule.source, '/api/v1/:path*');
  assert.match(rule.destination, /\/api\/v1\/:path\*$/);
});
