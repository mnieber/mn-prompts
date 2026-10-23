import { observer } from 'mobx-react-lite';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { authNav } from '/src/auth/routes';
import { history } from '/src/routes/history';
import { navTo } from '/src/routes/navHandler';

type PropsT = {};

const ContextProps = {
  authState: authStateCtx.authState,
};

export const RequireSignInEffect = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    React.useEffect(() => {
      if (!props.authState.isAuthenticated) {
        navTo(authNav.signIn({ nextUrl: history.location.pathname }));
      }
    });

    return null;
  }, ContextProps)
);
