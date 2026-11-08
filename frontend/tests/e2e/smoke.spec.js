import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

for (const [width,height] of [[320,700],[390,844],[768,1024],[1440,900],[1920,1080]]) {
  test(`landing, pricing and accessibility ${width}`, async ({page}) => {
    await page.setViewportSize({width,height});
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.goto('/');
    await expect(page.getByText('Backend and database connected.')).toBeVisible();
    await expect(page.getByText('AI planning is not configured yet.')).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.keyboard.press('Tab');
    await expect(page.getByText('Skip to content')).toBeFocused();
    expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
    await page.screenshot({path:`test-results/landing-${width}.png`,fullPage:true});
    await page.getByRole('link',{name:'Pricing',exact:true}).click();
    await expect(page.getByRole('heading',{name:'Plans are still taking shape.'})).toBeVisible();
    await expect(page.getByRole('button',{name:/buy|subscribe|trial/i})).toHaveCount(0);
    expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
    await page.screenshot({path:`test-results/pricing-${width}.png`,fullPage:true});
  });
}
