import { RequestHandler } from 'msw';
import { setupServer } from 'msw/node';

const beforeAll = (f: Function) => {
  console.log('Warning: using stub beforeAll');
};
const afterEach = (f: Function) => {
  console.log('Warning: using stub afterEach');
};
const afterAll = (f: Function) => {
  console.log('Warning: using stub afterAll');
};

export const testWithMsw = (
  handlers: RequestHandler[],
  testSuite: () => void
) => {
  const server = setupServer(...handlers);

  return () => {
    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());
    testSuite();
  };
};
