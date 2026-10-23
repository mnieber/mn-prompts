import { test as base, expect, type Page } from '@playwright/test';
import { FakeBackend } from '/tests/testEnv/FakeBackend';
import { endpoints } from '/tests/testEnv/endpoints';
import { apiUrl } from '/tests/testEnv/urls';

export type Ctx = {
  page: Page;
  backend: FakeBackend;
  pageErrors: Error[];
};

export const test = base.extend<{ ctx: Ctx }>({
  ctx: async ({ page }, use) => {
    const backend = new FakeBackend(apiUrl, endpoints);
    await backend.install(page);

    const pageErrors: Error[] = [];
    page.on('pageerror', (error) => pageErrors.push(error));

    await use({ page, backend, pageErrors });

    expect(backend.unexpectedRequests, 'unexpected api requests').toEqual([]);
    expect(pageErrors.map(String), 'uncaught errors in the page').toEqual([]);
  },
});
