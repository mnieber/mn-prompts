export function splitKeyHandlerKeys(keyHandlers: { [key: string]: Function }) {
  return Object.entries(keyHandlers).reduce((acc: any, [keys, f]) => {
    keys.split(';').forEach((key) => (acc[key] = f));
    return acc;
  }, {});
}

export function createKeyDownHandler(keyHandlers: { [key: string]: Function }) {
  return (key: string, e: any) => {
    const handler = keyHandlers[key];
    if (handler) {
      handler();
      e.preventDefault();
      e.stopPropagation();
    }
  };
}
