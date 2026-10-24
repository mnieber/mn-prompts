import type { FakeBackend } from '/tests/fakeBackend/FakeBackend';

export function signIn(backend: FakeBackend, userId: string) {
  backend.data.userId = userId;
}
