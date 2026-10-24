import { defineConfig, devices } from '@playwright/test';
import fs from 'fs';
import { apiUrl, baseURL, port } from './tests/testEnv/urls';

// The test packages are enabled in the order in which their code is implemented.
const enabledTestPackages = ['blogs', 'blogPosts'];

// Playwright's own browsers don't run on Alpine, so use the system chromium when it exists.
const systemChromium = '/usr/bin/chromium';

export default defineConfig({
  testDir: './tests',
  testMatch: enabledTestPackages.map((x) => `${x}/**/*.spec.ts`),
  fullyParallel: true,
  forbidOnly: true,
  retries: 0,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    ...devices['Desktop Chrome'],
    baseURL,
    locale: 'en-US',
    timezoneId: 'Europe/Amsterdam',
    viewport: { width: 1280, height: 800 },
    trace: 'retain-on-failure',
    launchOptions: fs.existsSync(systemChromium)
      ? { executablePath: systemChromium }
      : {},
  },
  webServer: {
    command: `yarn vite --mode test --port ${port} --strictPort`,
    url: baseURL,
    reuseExistingServer: true,
    env: { VITE_LOCALHOST_API_ENDPOINT: apiUrl },
  },
});
