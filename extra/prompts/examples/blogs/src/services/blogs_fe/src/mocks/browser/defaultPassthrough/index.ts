import { http, passthrough } from 'msw';
import { hostUrl } from '/src/api/restClient';

export const mapboxApiHandler = http.get('https://api.mapbox.com/*', () => {
  return passthrough();
});

export const mapboxEventsHandler = http.post(
  'https://events.mapbox.com/*',
  () => {
    return passthrough();
  }
);

export const blogs = http.get(`${hostUrl}*`, () => {
  return passthrough();
});

export const fonts = http.get('/fonts/*', () => {
  return passthrough();
});

export const src = http.get('/src/*', () => {
  return passthrough();
});

export const passthroughHandlers = [
  mapboxApiHandler,
  mapboxEventsHandler,
  blogs,
  fonts,
  src,
];
