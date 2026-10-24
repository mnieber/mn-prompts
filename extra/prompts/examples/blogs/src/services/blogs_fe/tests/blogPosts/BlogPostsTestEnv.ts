import { BlogsTestEnv } from '/tests/blogs/BlogsTestEnv';
import { addBlogPost } from '/tests/fakeBackend/actions';
import type { BlogPostRowT } from '/tests/fakeBackend/types';

export class BlogPostsTestEnv extends BlogsTestEnv {
  //
  // Actions
  //

  async addBlogPost(
    blogSlug: string,
    values: Omit<BlogPostRowT, 'id' | 'blog_id'>
  ) {
    addBlogPost(this.backend, blogSlug, values);
  }

  async clickBlogPost(title: string) {
    await this.blogPostListItem(title).click();
  }

  /** Adds the blog post to the selection (with ctrl-click). */
  async ctrlClickBlogPost(title: string) {
    await this.blogPostListItem(title).click({ modifiers: ['Control'] });
  }

  //
  // Queries
  //

  blogPostListItems() {
    return this.view('BlogPostListView').locator('.BlogPostListViewItem');
  }

  blogPostListItem(title: string) {
    return this.blogPostListItems().filter({ hasText: title });
  }
}
