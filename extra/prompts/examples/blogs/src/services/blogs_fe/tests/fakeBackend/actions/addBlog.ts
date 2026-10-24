import type { BlogRowT, FakeBackend } from '/tests/fakeBackend/FakeBackend';

export function addBlog(backend: FakeBackend, values: Omit<BlogRowT, 'id'>) {
  backend.data.blogs.push({ id: backend.nextId('blog'), ...values });
}
