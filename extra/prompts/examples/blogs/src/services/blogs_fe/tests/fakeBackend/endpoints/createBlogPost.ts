import type { BlogPostRowT, EndpointT } from '/tests/fakeBackend/types';

export const createBlogPost: EndpointT = {
  name: 'createBlogPost',
  method: 'POST',
  path: '/blogs/:blogId/blog-posts/create/',
  handle: (backend, request) => {
    if (!backend.data.blogs.some((x) => x.id === request.params.blogId)) {
      return { status: 404, json: ['BLOG_NOT_FOUND'] };
    }
    const form = request.body.create_blog_post_form;
    const blogPost: BlogPostRowT = {
      id: backend.nextId('blog-post'),
      blog_id: request.params.blogId,
      title: form.title,
      slug: form.slug,
      content: form.content ?? '',
      is_published: false,
      level: form.level ?? 'medium',
    };
    backend.data.blogPosts.push(blogPost);
    return { status: 200, json: blogPost };
  },
};
