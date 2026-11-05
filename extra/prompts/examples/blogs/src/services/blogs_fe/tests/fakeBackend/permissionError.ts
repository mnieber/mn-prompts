import type { FakeBackend } from '/tests/fakeBackend/FakeBackend';
import type { ResponseT } from '/tests/fakeBackend/types';

/** The response of the real backend when the user isn't allowed to do this. */
export const permissionError = (): ResponseT => {
  return { status: 403, json: { detail: 'You must be the blog owner.' } };
};

export const isBlogOwner = (backend: FakeBackend, blogId: string) => {
  return (
    backend.data.blogs.find((x) => x.id === blogId)?.owner_id ===
    backend.data.userId
  );
};
