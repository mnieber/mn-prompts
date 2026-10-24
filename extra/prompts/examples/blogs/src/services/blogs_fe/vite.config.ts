import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import checker from 'vite-plugin-checker';

// The playground server (yarn fake) listens on this port. See tests/fakeBackend/urls.ts.
const playgroundPort = 3200;

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), checker({ typescript: true })],
  resolve: {
    conditions: ['development'],
  },
  esbuild: {
    // The npm overlays in /npm are compiled with the tsconfig settings below.
    // Without useDefineForClassFields, an uninitialized field such as `@data item?: T`
    // is not emitted, and then MobX silently skips making it observable.
    tsconfigRaw: {
      compilerOptions: {
        experimentalDecorators: true,
        useDefineForClassFields: true,
      },
    },
  },
  server: {
    port: 3000,
    proxy: {
      // When flags.useFakeBackend is true, the app sends its api requests to the playground
      '/fake-api/': {
        target: `http://localhost:${playgroundPort}`,
        configure: (proxy) => {
          proxy.on('error', (error, request, response) => {
            console.warn(
              `No fake backend on :${playgroundPort} for ${request.url}. Run yarn fake <playground>.`
            );
            if ('writeHead' in response && !response.headersSent) {
              response.writeHead(502, { 'Content-Type': 'application/json' });
              response.end(JSON.stringify(['NO_FAKE_BACKEND']));
            }
          });
        },
      },
    },
  },
});
