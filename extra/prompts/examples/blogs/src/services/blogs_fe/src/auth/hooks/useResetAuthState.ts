import React from 'react';
import { AuthState } from '/src/auth/AuthState';

export const useResetAuthState = (authState: AuthState) => {
  React.useEffect(() => {
    authState.reset();
  }, [authState]);
};
