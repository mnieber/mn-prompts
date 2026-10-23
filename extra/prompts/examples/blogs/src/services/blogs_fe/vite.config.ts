import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import checker from 'vite-plugin-checker';

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
  },
});
