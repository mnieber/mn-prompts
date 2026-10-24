import { JUDO } from '/tests/blogs/fixtures';
import { addBlog, signIn } from '/tests/fakeBackend/actions';
import type { PlaygroundT } from '/tests/playgrounds/PlaygroundT';

export const playground: PlaygroundT = {
  description:
    'A signed-in user who has the blog Judo presses Create blog to create a new blog.',
  // Opening /blogs/create/_ directly redirects to the sign-in page, because
  // RequireSignInEffect runs before the user id is loaded.
  url: '/blogs',
  setUp: (backend) => {
    signIn(backend, 'user-1');
    addBlog(backend, JUDO);
  },
};
