import type { EndpointT } from '/tests/fakeBackend/types';
import { validationError } from '/tests/fakeBackend/validationError';

export const getBlogPosts: EndpointT = {
  name: 'getBlogPosts',
  method: 'GET',
  path: '/blogs/:blogSlug/blog-posts/list/',
  handle: (backend, request) => {
    const blog = backend.data.blogs.find(
      (x) => x.slug === request.params.blogSlug
    );
    if (!blog) {
      return validationError('BLOG_NOT_FOUND');
    }
    const blogPosts = backend.data.blogPosts.filter(
      (x) => x.blog_id === blog.id
    );
    return { status: 200, json: blogPosts };
  },
};
