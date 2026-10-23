export function wait<T>(ms: number, value: T) {
  return new Promise<T>((resolve) => setTimeout(resolve, ms, value));
}

export function waitOnDev<T>(ms: number, value: T) {
  // No simulated latency in the tests
  const isDev = import.meta.env.DEV && import.meta.env.MODE !== 'test';
  return wait(isDev ? ms : 0, value);
}
