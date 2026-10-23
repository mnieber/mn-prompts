import * as R from 'ramda';
import React from 'react';
import { NavState } from '/src/routes/NavState/NavState';

export const NavStateContext = React.createContext<any>(null);

export const useNavStateContext = () => {
  const context = React.useContext(NavStateContext);
  if (!context) {
    throw new Error(
      'useNavStateContext must be used within a NavStateContext.Provider'
    );
  }
  return context;
};

export const navStateCtx = R.mergeAll([
  {
    navState: [
      //
      useNavStateContext,
      'navState',
    ] as any as NavState,
  },
]);
