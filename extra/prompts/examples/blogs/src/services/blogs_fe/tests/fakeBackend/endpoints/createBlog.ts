import { generateUniqueSlug } from '/tests/fakeBackend/generateUniqueSlug';
import { hasForbiddenWords } from '/tests/fakeBackend/hasForbiddenWords';
import type { BlogRowT, EndpointT } from '/tests/fakeBackend/types';
import { validationError } from '/tests/fakeBackend/validationError';

export const createBlog: EndpointT = {
  name: 'createBlog',
  method: 'POST',
  path: '/blogs/create/',
  handle: (backend, request) => {
    const form = request.body.create_blog_form;
    if (
      backend.data.blogs.some(
        (x) => x.name.toLowerCase() === form.name.toLowerCase()
      )
    ) {
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
      slug: generateUniqueSlug(
        form.name,
        'blog',
        backend.data.blogs.map((x) => x.slug)
      ),
      description: form.description ?? null,
      owner_id: backend.data.userId ?? '',
    };
    backend.data.blogs.push(blog);
    return { status: 201, json: blog };
  },
};
