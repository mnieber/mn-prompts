import { hasForbiddenWords } from '/tests/fakeBackend/hasForbiddenWords';
import type { EndpointT } from '/tests/fakeBackend/types';
import { validationError } from '/tests/fakeBackend/validationError';

export const updateBlogPost: EndpointT = {
  name: 'updateBlogPost',
  method: 'POST',
  path: '/blogs/:blogId/blog-posts/:blogPostId/update/',
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
    const form = request.body.update_blog_post_form;
    if (
      backend.data.blogPosts.some(
        (x) =>
          x.blog_id === request.params.blogId &&
          x.id !== blogPost.id &&
          x.title === form.title
      )
    ) {
      return validationError('BLOG_POST_TITLE_ALREADY_EXISTS');
    }
    if (hasForbiddenWords(form.title)) {
      return validationError('FORM_CONTAINS_FORBIDDEN_WORDS', 'title');
    }
    if (hasForbiddenWords(form.content)) {
      return validationError('FORM_CONTAINS_FORBIDDEN_WORDS', 'content');
    }
    blogPost.title = form.title ?? blogPost.title;
    blogPost.slug = form.slug ?? blogPost.slug;
    blogPost.content = form.content ?? blogPost.content;
    blogPost.level = form.level ?? blogPost.level;
    return { status: 200, json: blogPost };
  },
};
