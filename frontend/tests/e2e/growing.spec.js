import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

for (const [width,height] of [[320,700],[390,844],[768,1024],[1440,900],[1920,1080]]) {
  test(`account and resumable plot ${width}`,async ({page}) => {
    await page.setViewportSize({width,height});
    const email = `browser-${width}-${Date.now()}@example.com`;
    const password = 'local browser test password';
    await page.goto('/signup');
    await page.getByLabel('Email',{exact:true}).fill(email);
    await page.getByLabel('Password',{exact:true}).fill(password);
    await page.getByRole('button',{name:'Create account',exact:true}).click();
    await expect(page.getByRole('heading',{name:'No plots saved yet.'})).toBeVisible();
    if (width < 900) {
      await page.getByRole('button',{name:'Garden menu',exact:true}).click();
      await expect(page.getByRole('dialog',{name:'Garden menu'})).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(page.getByRole('button',{name:'Garden menu',exact:true})).toBeFocused();
    }
    await page.getByRole('link',{name:'Set up your first plot'}).click();
    await page.getByLabel('Plot name',{exact:true}).fill('Synthetic test garden');
    await page.getByRole('button',{name:'Save draft',exact:true}).click();
    await expect(page.getByRole('status')).toContainText('Draft saved');
    await page.reload();
    await expect(page.getByLabel('Plot name',{exact:true})).toHaveValue('Synthetic test garden');
    await page.getByLabel('Area (m²)',{exact:true}).fill('12.5');
    await page.getByLabel('Growing region',{exact:true}).fill('Central Texas');
    await page.getByLabel('Season name',{exact:true}).fill('Spring');
    await page.getByLabel('Season year',{exact:true}).fill('2027');
    expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
    await page.screenshot({path:`test-results/onboarding-${width}.png`,fullPage:true});
    await page.getByRole('button',{name:'Save and continue'}).click();
    await expect(page.getByRole('heading',{name:'What you know so far.'})).toBeVisible();
    await page.getByRole('button',{name:'Save and continue'}).click();
    await expect(page.getByRole('heading',{name:'Review your growing record.'})).toBeVisible();
    await page.getByRole('button',{name:'Save plot and season'}).click();
    await expect(page.getByRole('heading',{name:'Synthetic test garden'})).toBeVisible();
    await expect(page.getByText('Unknown — no measurement entered')).toBeVisible();
    await page.getByRole('button',{name:'Edit plot details'}).click();
    await page.getByLabel('Area (m²)',{exact:true}).fill('16');
    await page.getByRole('button',{name:'Save plot details'}).click();
    await expect(page.getByText('16 m²',{exact:true})).toBeVisible();
    await expect(page.getByRole('button',{name:'Generate a plan'})).toBeDisabled();
    expect(page.url()).toMatch(/plot_id=.*season_id=/);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
    await page.screenshot({path:`test-results/dashboard-${width}.png`,fullPage:true});
    await page.getByRole('button',{name:'Log out',exact:true}).click();
    await expect(page.getByRole('heading',{name:'Welcome back.'})).toBeVisible();
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/\/login$/);
    await page.getByLabel('Email',{exact:true}).fill(email);
    await page.getByLabel('Password',{exact:true}).fill(password);
    await page.getByRole('button',{name:'Log in',exact:true}).click();
    await expect(page.getByRole('heading',{name:'Synthetic test garden'})).toBeVisible();
    const challenge = await (await page.request.get('/api/v1/auth/csrf')).json();
    const removal = await page.request.delete('/api/v1/auth/me',{headers:{Origin:new URL(page.url()).origin,'X-CSRF-Token':challenge.csrf_token}});
    expect(removal.status()).toBe(204);
  });
}
