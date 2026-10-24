import { addBlog } from '/tests/fakeBackend/actions';
import type { BlogRowT } from '/tests/fakeBackend/types';
import { TestEnv } from '/tests/testEnv/TestEnv';

export class BlogsTestEnv extends TestEnv {
  //
  // Actions
  //

  async addBlog(values: Omit<BlogRowT, 'id'>) {
    addBlog(this.backend, values);
  }

  //
  // Queries
  //

  blogListItems() {
    return this.view('BlogListView').locator('.BlogListViewItem');
  }

  blogListItem(name: string) {
    return this.view('BlogListView').getByRole('link', { name, exact: true });
  }
}
