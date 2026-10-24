// Maps the `/src/...` and `/tests/...` imports (see tests/tsconfig.json) to the project
// folder, so that the playgrounds can run in Node.
import path from 'path';
import { pathToFileURL } from 'url';

const root = path.resolve(import.meta.dirname, '../..');

export async function resolve(specifier, context, nextResolve) {
  if (/^\/(src|tests)\//.test(specifier)) {
    return nextResolve(pathToFileURL(path.join(root, specifier)).href, context);
  }
  return nextResolve(specifier, context);
}
