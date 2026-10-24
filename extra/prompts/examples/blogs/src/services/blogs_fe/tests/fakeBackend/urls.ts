// The app sends its api requests to this path, and the FakeBackend answers them.
// This path must match the fakeApiUrl in src/api/restClient.ts.
export const fakeApiPath = '/fake-api/';

// The playground server (yarn fake) listens here, and vite proxies the fakeApiPath to it.
export const playgroundPort = 3200;
