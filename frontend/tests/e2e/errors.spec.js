import { test, expect } from '@playwright/test';

test('backend and database failures have truthful states', async ({page}) => {
  await page.route('**/api/v1/health', route => route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({database:'unavailable'})}));
  await page.goto('/');
  await expect(page.getByRole('status')).toContainText('Database unavailable');
  await page.route('**/api/v1/health', route => route.abort());
  await page.reload();
  await expect(page.getByRole('status')).toContainText('Backend unavailable');
  await expect(page.getByText('AI planning is not configured yet.')).toBeVisible();
});

test('soil validation and stale drafts keep entered values', async ({page}) => {
  await page.goto('/signup');
  await page.getByLabel('Email',{exact:true}).fill(`errors-${Date.now()}@example.com`);
  await page.getByLabel('Password',{exact:true}).fill('local browser test password');
  await page.getByRole('button',{name:'Create account',exact:true}).click();
  await page.getByRole('link',{name:'Set up your first plot'}).click();
  await page.getByLabel('Plot name',{exact:true}).fill('Unsaved test plot');
  await page.getByRole('button',{name:'Save and continue'}).click();
  await page.getByLabel('Soil pH (optional)',{exact:true}).fill('6.5');
  await page.getByRole('button',{name:'Save draft',exact:true}).click();
  await expect(page.getByRole('alert').filter({hasText:'Add the observation date'})).toBeVisible();
  await expect(page.getByLabel('Soil pH (optional)',{exact:true})).toHaveValue('6.5');
  await page.getByLabel('Soil observation date',{exact:true}).fill('2026-01-01');
  const token = (await (await page.request.get('/api/v1/auth/csrf')).json()).csrf_token;
  const headers = {Origin:new URL(page.url()).origin,'X-CSRF-Token':token};
  const saved = await page.request.put('/api/v1/onboarding/draft',{headers,data:{expected_revision:1,step:2,draft_data:{plot_name:'Changed in another tab'}}});
  expect(saved.status()).toBe(200);
  await page.getByRole('button',{name:'Save draft',exact:true}).click();
  await expect(page.getByRole('alert').filter({hasText:'changed in another tab'})).toBeVisible();
  await expect(page.getByLabel('Soil pH (optional)',{exact:true})).toHaveValue('6.5');
  expect((await page.request.delete('/api/v1/auth/me',{headers})).status()).toBe(204);
});
