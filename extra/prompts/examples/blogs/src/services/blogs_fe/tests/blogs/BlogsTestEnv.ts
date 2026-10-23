import type { BlogRowT } from '/tests/testEnv/FakeBackend';
import { TestEnv } from '/tests/testEnv/TestEnv';

export class BlogsTestEnv extends TestEnv {
  //
  // Actions
  //

  async addBlog(values: Omit<BlogRowT, 'id'>) {
    this.backend.data.blogs.push({
      id: this.backend.nextId('blog'),
      ...values,
    });
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
