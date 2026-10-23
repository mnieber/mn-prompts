import type { Page } from '@playwright/test';
import type { FakeBackend } from '/tests/testEnv/FakeBackend';
import type { Ctx } from '/tests/testEnv/fixtures';

export class TestEnv {
  page: Page;
  backend: FakeBackend;
  pageErrors: Error[];

  constructor(ctx: Ctx) {
    this.page = ctx.page;
    this.backend = ctx.backend;
    this.pageErrors = ctx.pageErrors;
    this.postInit();
  }

  protected postInit() {}

  step(..._: unknown[]) {
    return true;
  }

  //
  // Actions
  //

  async signIn(userId: string) {
    this.backend.data.userId = userId;
  }

  /** Opens the url, and waits until the app has rendered. */
  async visit(url: string) {
    await this.page.goto(url);
    await this.page.locator('#App').waitFor();
  }

  async clickButton(name: string) {
    await this.button(name).click();
  }

  /** Fills the form field that has the given label. */
  async fillField(label: string, value: string) {
    await this.page.getByLabel(label, { exact: true }).fill(value);
  }

  //
  // Queries
  //

  /** The root element of the component with the given name. */
  view(name: string) {
    return this.page.locator(`.${name}`);
  }

  button(name: string) {
    return this.page.getByRole('button', { name, exact: true });
  }
}
