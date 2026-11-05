import {
  isBlogOwner,
  permissionError,
} from '/tests/fakeBackend/permissionError';
import type { EndpointT } from '/tests/fakeBackend/types';
import { validationError } from '/tests/fakeBackend/validationError';

export const deleteBlogPosts: EndpointT = {
  name: 'deleteBlogPosts',
  method: 'POST',
  path: '/blogs/:blogId/blog-posts/delete/',
  handle: (backend, request) => {
    if (!isBlogOwner(backend, request.params.blogId)) {
      return permissionError();
    }
    const ids: string[] = request.body.delete_blog_posts_form.blog_post_ids;
    const blogPosts = backend.data.blogPosts.filter(
      (x) => x.blog_id === request.params.blogId && ids.includes(x.id)
    );
    if (blogPosts.length !== ids.length) {
      return validationError('BLOG_POSTS_NOT_FOUND');
    }
    backend.data.blogPosts = backend.data.blogPosts.filter(
      (x) => !blogPosts.includes(x)
    );
    return { status: 204 };
  },
};
