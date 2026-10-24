import type { BlogRowT, EndpointT } from '/tests/fakeBackend/FakeBackend';

export const createBlog: EndpointT = {
  name: 'createBlog',
  method: 'POST',
  path: '/blogs/create/',
  handle: (backend, request) => {
    const form = request.body.create_blog_form;
    if (backend.data.blogs.some((x) => x.name === form.name)) {
      return { status: 400, json: ['BLOG_WITH_NAME_EXISTS'] };
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
