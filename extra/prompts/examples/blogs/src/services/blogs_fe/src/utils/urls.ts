export const joinUrls = (lhs: string, rhs: string) => {
  if (lhs.endsWith('/') && rhs.startsWith('/')) {
    return lhs + rhs.substring(1);
  } else if (!lhs.endsWith('/') && !rhs.startsWith('/')) {
    return lhs + '/' + rhs;
  } else {
    return lhs + rhs;
  }
};

export const pathname = () => {
  const result = window.location.pathname;
  return chopTrailingSlash(result);
};

export function chopTrailingSlash(result: string) {
  return result.endsWith('/') ? result.slice(0, result.length - 1) : result;
}
