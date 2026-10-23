export const createQueryKey = <T>(
  name: string,
  x?: T
): [string, T] | [string] => {
  return x === undefined ? [name] : [name, x];
};
