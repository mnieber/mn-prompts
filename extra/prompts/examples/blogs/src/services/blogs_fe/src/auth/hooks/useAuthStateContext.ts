import * as R from 'ramda';
import React from 'react';
import { AuthState } from '/src/auth/AuthState';

export const AuthStateContext = React.createContext<any>(null);

export const useAuthStateContext = () => {
  const context = React.useContext(AuthStateContext);
  if (!context) {
    throw new Error(
      'useAuthStateContext must be used within a AuthStateContext.Provider'
    );
  }
  return context;
};

export const authStateCtx = R.mergeAll([
  {
    authState: [useAuthStateContext, 'authState'] as any as AuthState,
  },
]);
