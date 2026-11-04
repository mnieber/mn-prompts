import { hasForbiddenWords } from '/tests/fakeBackend/hasForbiddenWords';
import type { BlogPostRowT, EndpointT } from '/tests/fakeBackend/types';
import { validationError } from '/tests/fakeBackend/validationError';

export const createBlogPost: EndpointT = {
  name: 'createBlogPost',
  method: 'POST',
  path: '/blogs/:blogId/blog-posts/create/',
  handle: (backend, request) => {
    if (!backend.data.blogs.some((x) => x.id === request.params.blogId)) {
      return validationError('BLOG_NOT_FOUND');
    }
    const form = request.body.create_blog_post_form;
    if (
      backend.data.blogPosts.some(
        (x) => x.blog_id === request.params.blogId && x.title === form.title
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
