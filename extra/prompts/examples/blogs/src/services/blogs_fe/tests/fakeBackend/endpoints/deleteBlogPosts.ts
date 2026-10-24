import type { EndpointT } from '/tests/fakeBackend/types';

export const deleteBlogPosts: EndpointT = {
  name: 'deleteBlogPosts',
  method: 'POST',
  path: '/blogs/:blogId/blog-posts/delete/',
  handle: (backend, request) => {
    const ids: string[] = request.body.delete_blog_posts_form.blog_post_ids;
    const blogPosts = backend.data.blogPosts.filter(
      (x) => x.blog_id === request.params.blogId && ids.includes(x.id)
    );
    if (blogPosts.length !== ids.length) {
      return { status: 404, json: ['BLOG_POSTS_NOT_FOUND'] };
    }
    backend.data.blogPosts = backend.data.blogPosts.filter(
      (x) => !blogPosts.includes(x)
    );
    return { status: 200, json: {} };
  },
};
