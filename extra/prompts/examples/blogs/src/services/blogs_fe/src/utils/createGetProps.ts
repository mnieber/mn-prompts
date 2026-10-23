export const createGetProps = (obj: { [key: string]: any }) => {
  const getters = {};
  for (const key in obj) {
    Object.defineProperty(getters, key, {
      get: obj[key],
      enumerable: true,
      configurable: true,
    });
  }
  return getters;
};
