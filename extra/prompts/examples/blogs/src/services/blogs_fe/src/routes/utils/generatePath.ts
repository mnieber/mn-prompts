import { ObjT } from '/src/utils/types';

export function generatePath(pattern: string, params: ObjT = {}): string {
  return pattern.replace(/:(\w+)|(?:\*)/g, (match, key) => {
    if (match === '*') {
      return params['*'] || '';
    }

    if (params[key] === undefined) {
      throw new Error(`Missing "${key}" parameter for path "${pattern}"`);
    }

    return params[key];
  });
}
