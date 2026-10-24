import type { FakeBackend } from '/tests/fakeBackend/FakeBackend';
import type { BlogRowT } from '/tests/fakeBackend/types';

export function addBlog(backend: FakeBackend, values: Omit<BlogRowT, 'id'>) {
  backend.data.blogs.push({ id: backend.nextId('blog'), ...values });
}
