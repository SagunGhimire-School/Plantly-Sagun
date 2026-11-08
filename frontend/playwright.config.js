import { defineConfig } from '@playwright/test';

const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000';
export default defineConfig({
  testDir:'./tests/e2e', fullyParallel:false, workers:1,
  use:{baseURL, trace:'retain-on-failure'},
  webServer:{command:`node node_modules/next/dist/bin/next dev --hostname 127.0.0.1 --port ${new URL(baseURL).port || 3000}`, url:baseURL, reuseExistingServer:true, timeout:120000},
});
