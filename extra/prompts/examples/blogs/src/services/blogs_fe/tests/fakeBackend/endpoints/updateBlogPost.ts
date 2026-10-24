import type { EndpointT } from '/tests/fakeBackend/types';

export const updateBlogPost: EndpointT = {
  name: 'updateBlogPost',
  method: 'POST',
  path: '/blogs/:blogId/blog-posts/:blogPostId/update/',
  handle: (backend, request) => {
    if (!backend.data.blogs.some((x) => x.id === request.params.blogId)) {
      return { status: 404, json: ['BLOG_NOT_FOUND'] };
    }
    const blogPost = backend.data.blogPosts.find(
      (x) =>
        x.id === request.params.blogPostId &&
        x.blog_id === request.params.blogId
    );
    if (!blogPost) {
      return { status: 404, json: ['BLOG_POST_NOT_FOUND'] };
    }
    const form = request.body.update_blog_post_form;
    blogPost.title = form.title ?? blogPost.title;
    blogPost.slug = form.slug ?? blogPost.slug;
    blogPost.content = form.content ?? blogPost.content;
    blogPost.level = form.level ?? blogPost.level;
    return { status: 200, json: blogPost };
  },
};
