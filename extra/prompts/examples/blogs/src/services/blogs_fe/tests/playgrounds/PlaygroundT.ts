import type { FakeBackend } from '/tests/fakeBackend/FakeBackend';

export type PlaygroundT = {
  description: string;
  // The page to open first
  url: string;
  // Fills the fake backend with the data of the playground
  setUp: (backend: FakeBackend) => void;
};
