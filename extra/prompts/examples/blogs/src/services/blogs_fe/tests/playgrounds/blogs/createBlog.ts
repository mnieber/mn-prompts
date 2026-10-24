import { JUDO } from '/tests/blogs/exampleData';
import { addBlog, signIn } from '/tests/fakeBackend/actions';
import type { PlaygroundT } from '/tests/playgrounds/PlaygroundT';

export const playground: PlaygroundT = {
  description: 'A signed-in user who has the blog Judo creates a new blog.',
  url: '/blogs/create/_',
  setUp: (backend) => {
    signIn(backend, 'user-1');
    addBlog(backend, JUDO);
  },
};
