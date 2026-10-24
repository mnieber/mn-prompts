import axios from 'axios';
import { flags } from '/src/app/flags';

axios.defaults.withCredentials = true;

// Vite proxies this path to the playground server (see tests/playgrounds)
const fakeApiUrl = '/fake-api/';

export const hostUrl =
  import.meta.env.DEV && flags.useFakeBackend
    ? fakeApiUrl
    : window.location.host.startsWith('localhost')
      ? import.meta.env.VITE_LOCALHOST_API_ENDPOINT
      : (import.meta.env.VITE_BACKEND_API_ENDPOINT ?? '');

export function get(query: string) {
  return axios
    .get(`${hostUrl}${trimLeadingSlash(query)}`, {
      headers: getHeaders(),
    })
    .then((response) => {
      return response;
    });
}

export function post(query: string, variables: any, headers?: any) {
  const allHeaders = {
    ...getHeaders(),
    ...(headers ?? {}),
  };

  return axios
    .post(`${hostUrl}${trimLeadingSlash(query)}`, variables, {
      headers: allHeaders,
    })
    .then((response) => {
      return response;
    });
}

function getHeaders() {
  const accessToken = getAccessToken();
  return accessToken
    ? {
        Authorization: `Bearer ${accessToken}`,
      }
    : {};
}

function trimLeadingSlash(query: string) {
  if (query.startsWith('/') && hostUrl.endsWith('/')) {
    query = query.substring(1);
  }
  return query;
}

export const setAuthTokens = (
  accessToken: string | undefined,
  refreshToken?: string
) => {
  if (accessToken === undefined) {
    localStorage.removeItem('accessToken');
  } else {
    localStorage.setItem('accessToken', accessToken);
  }
  if (refreshToken === undefined) {
    localStorage.removeItem('refreshToken');
  } else {
    localStorage.setItem('refreshToken', refreshToken);
  }
};

export const getAccessToken = () => {
  return localStorage.getItem('accessToken');
};

export const getRefreshToken = () => {
  return localStorage.getItem('refreshToken');
};
