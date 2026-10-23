import React from 'react';

export const useBuilder = <T>(builder: () => T): T => {
  const ref = React.useRef<T | null>(null);
  if (ref.current === null) {
    ref.current = builder();
  }
  return ref.current as T;
};
