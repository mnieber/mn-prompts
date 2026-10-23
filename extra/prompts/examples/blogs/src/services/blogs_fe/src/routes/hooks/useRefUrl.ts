import React from 'react';
import { useLocation } from 'wouter';

export const useRefUrl = () => {
  const [location] = useLocation();
  const refUrl = React.useRef<string>('');
  const updateRefUrl = () => (refUrl.current = location);
  return {
    hasUrlChanged: refUrl.current !== location,
    updateRefUrl,
  };
};
