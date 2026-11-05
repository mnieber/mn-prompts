import type { FakeBackend } from '/tests/fakeBackend/FakeBackend';
import type { BlogRowT } from '/tests/fakeBackend/types';

/** Adds a blog. Its owner is the signed-in user, unless the values say otherwise. */
export function addBlog(
  backend: FakeBackend,
  values: Omit<BlogRowT, 'id' | 'owner_id'> & { owner_id?: string }
) {
  backend.data.blogs.push({
    id: backend.nextId('blog'),
    owner_id: backend.data.userId ?? '',
    ...values,
  });
}
