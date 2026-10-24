import { fakeApiPath } from '/tests/fakeBackend/urls';

export const port = 3100;
export const baseURL = `http://localhost:${port}`;
// The FakeBackend intercepts the api requests to this url.
export const apiUrl = `${baseURL}${fakeApiPath}`;
