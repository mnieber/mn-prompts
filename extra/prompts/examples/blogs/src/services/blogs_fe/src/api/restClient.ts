import axios from 'axios';
import { flags } from '/src/app/flags';

// Django sets this cookie, and checks this header on each write
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// Vite proxies this path to the playground server (see tests/playgrounds). In the
// tests, the FakeBackend intercepts the requests to this path.
const fakeApiUrl = '/fake-api/';

export const hostUrl =
  import.meta.env.MODE === 'test' ||
  (import.meta.env.DEV && flags.useFakeBackend)
    ? fakeApiUrl
    : '/api/';

export function get(query: string) {
  return detectExpiredSession(authGet(query));
}

export function post(query: string, variables: any, headers?: any) {
  return detectExpiredSession(authPost(query, variables, headers));
}

// The auth endpoints use the functions below. They don't detect an expired session,
// because a 401 is a normal response of these endpoints.
export function authGet(query: string) {
  return axios.get(`${hostUrl}${trimLeadingSlash(query)}`);
}

export function authPost(query: string, variables: any, headers?: any) {
  return axios.post(`${hostUrl}${trimLeadingSlash(query)}`, variables, {
    headers,
  });
}

export function authDelete(query: string) {
  return axios.delete(`${hostUrl}${trimLeadingSlash(query)}`);
}

let onSessionExpired = () => {};

export const setOnSessionExpired = (callback: () => void) => {
  onSessionExpired = callback;
};

function detectExpiredSession(request: Promise<any>) {
  return request.catch((error) => {
    if (error.response?.status === 401) {
      onSessionExpired();
    }
    throw error;
  });
}

function trimLeadingSlash(query: string) {
  if (query.startsWith('/') && hostUrl.endsWith('/')) {
    query = query.substring(1);
  }
  return query;
}
