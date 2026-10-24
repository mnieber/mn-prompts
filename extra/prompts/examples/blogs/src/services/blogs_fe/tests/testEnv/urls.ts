export const port = 3100;
export const baseURL = `http://localhost:${port}`;
// The app sends its api requests here, and the FakeBackend intercepts them.
// This path must match the fakeApiUrl in src/api/restClient.ts.
export const fakeApiPath = '/fake-api/';
export const apiUrl = `${baseURL}${fakeApiPath}`;

// The playground server (yarn fake) listens here, and vite proxies the fakeApiPath to it.
export const playgroundPort = 3200;
// The port of the vite dev server that the playground is used with.
export const devServerPort = 3000;
