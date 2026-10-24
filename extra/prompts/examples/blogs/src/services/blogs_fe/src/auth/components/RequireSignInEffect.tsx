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
    // Wait until we know whether the user is signed in. Note that we read the
    // observables here (and not in the effect), so that the observer tracks them.
    const mustSignIn =
      props.authState.isUserIdKnown && !props.authState.isAuthenticated;

    React.useEffect(() => {
      if (mustSignIn) {
        navTo(authNav.signIn({ nextUrl: history.location.pathname }));
      }
    });

    return null;
  }, ContextProps)
);
