import type { FakeBackend } from '/tests/fakeBackend/FakeBackend';
import type { BlogPostRowT } from '/tests/fakeBackend/types';

/** Adds a blog post to the blog with the given slug. */
export function addBlogPost(
  backend: FakeBackend,
  blogSlug: string,
  values: Omit<BlogPostRowT, 'id' | 'blog_id'>
) {
  const blog = backend.data.blogs.find((x) => x.slug === blogSlug);
  if (!blog) {
    throw new Error(`There is no blog with slug ${blogSlug}`);
  }
  backend.data.blogPosts.push({
    id: backend.nextId('blog-post'),
    blog_id: blog.id,
    ...values,
  });
}
