import { hasForbiddenWords } from '/tests/fakeBackend/hasForbiddenWords';
import type { BlogRowT, EndpointT } from '/tests/fakeBackend/types';
import { validationError } from '/tests/fakeBackend/validationError';

export const createBlog: EndpointT = {
  name: 'createBlog',
  method: 'POST',
  path: '/blogs/create/',
  handle: (backend, request) => {
    const form = request.body.create_blog_form;
    if (backend.data.blogs.some((x) => x.name === form.name)) {
      return validationError('BLOG_NAME_ALREADY_EXISTS');
    }
    if (hasForbiddenWords(form.name)) {
      return validationError('FORM_CONTAINS_FORBIDDEN_WORDS', 'name');
    }
    if (hasForbiddenWords(form.description)) {
      return validationError('FORM_CONTAINS_FORBIDDEN_WORDS', 'description');
    }
    const blog: BlogRowT = {
      id: backend.nextId('blog'),
      name: form.name,
      slug: form.slug,
      description: form.description ?? '',
    };
    backend.data.blogs.push(blog);
    return { status: 200, json: blog };
  },
};
