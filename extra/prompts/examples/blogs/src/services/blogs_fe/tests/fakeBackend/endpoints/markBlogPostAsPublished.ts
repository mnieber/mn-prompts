import {
  isBlogOwner,
  permissionError,
} from '/tests/fakeBackend/permissionError';
import type { EndpointT } from '/tests/fakeBackend/types';
import { validationError } from '/tests/fakeBackend/validationError';

export const markBlogPostAsPublished: EndpointT = {
  name: 'markBlogPostAsPublished',
  method: 'POST',
  path: '/blogs/:blogId/blog-posts/:blogPostId/publish/',
  handle: (backend, request) => {
    if (!backend.data.blogs.some((x) => x.id === request.params.blogId)) {
      return validationError('BLOG_NOT_FOUND');
    }
    const blogPost = backend.data.blogPosts.find(
      (x) =>
        x.id === request.params.blogPostId &&
        x.blog_id === request.params.blogId
    );
    if (!blogPost) {
      return validationError('BLOG_POST_NOT_FOUND');
    }
    if (!isBlogOwner(backend, request.params.blogId)) {
      return permissionError();
    }
    blogPost.is_published = true;
    return { status: 200, json: blogPost };
  },
};
