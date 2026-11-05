import React from 'react';
import { observer } from 'mobx-react-lite';
import { setOnSessionExpired } from '/src/api/restClient';
import { anonymous, AuthState } from '/src/auth/AuthState';
import { useLoadUserId } from '/src/auth/endpoints/queries';
import { States } from '/src/auth/endpoints/states';
import { AuthStateContext } from '/src/auth/hooks/useAuthStateContext';
import { authNav } from '/src/auth/routes';
import { history } from '/src/routes/history';
import { navTo } from '/src/routes/navHandler';
import { createGetProps } from '/src/utils/createGetProps';
import { useBuilder } from '/src/utils/hooks/useBuilder';

type PropsT = React.PropsWithChildren<{}>;

export const AuthStateProvider = observer((props: PropsT) => {
  const authState = useBuilder(() => new AuthState(States.INITIAL));
  useLoadUserId(authState);

  React.useEffect(() => {
    setOnSessionExpired(() => {
      if (authState.isAuthenticated) {
        authState.setUserId(anonymous);
        navTo(authNav.signIn({ nextUrl: history.location.pathname }));
      }
    });
  }, [authState]);

  const getAuthStateContext = () => {
    return createGetProps({
      authState: () => authState,
    });
  };

  return (
    <AuthStateContext.Provider value={getAuthStateContext()}>
      {props.children}
    </AuthStateContext.Provider>
  );
});
