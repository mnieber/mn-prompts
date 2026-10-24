import type { BlogRowT, FakeBackend } from '/tests/testEnv/FakeBackend';

export const JUDO = {
  name: 'Judo',
  slug: 'judo',
  description: 'Throws and pins.',
};

export function addBlog(backend: FakeBackend, values: Omit<BlogRowT, 'id'>) {
  backend.data.blogs.push({ id: backend.nextId('blog'), ...values });
}
