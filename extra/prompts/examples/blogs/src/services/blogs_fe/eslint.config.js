import js from '@eslint/js';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist', 'playwright-report', 'test-results'] },
  {
    files: ['src/**/*.{ts,tsx}', 'tests/**/*.ts'],
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    languageOptions: { ecmaVersion: 'latest' },
    rules: {
      // Our conventions use `any` (e.g. in the context selectors) and `{}` (e.g. `PropsT = {}`)
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-empty-object-type': 'off',
      // We use `Function` as the type of a callback
      '@typescript-eslint/no-unsafe-function-type': 'off',
      // Unused function arguments are part of an interface (e.g. `callerId` of a nav handler).
      // Unused rest siblings remove props (e.g. `const { className, ...rest } = props`).
      '@typescript-eslint/no-unused-vars': [
        'error',
        { args: 'none', caughtErrors: 'none', ignoreRestSiblings: true },
      ],
    },
  },
  {
    // The app
    files: ['src/**/*.{ts,tsx}'],
    languageOptions: { globals: globals.browser },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      // Component files also export their ContextProps
      'react-refresh/only-export-components': 'off',
    },
  },
  {
    // The tests and playgrounds run in Node
    files: ['tests/**/*.ts'],
    languageOptions: { globals: globals.node },
    rules: {
      // A test step without asserts has an empty body: `if (env.step(...)) {}`
      'no-empty': 'off',
    },
  }
);
