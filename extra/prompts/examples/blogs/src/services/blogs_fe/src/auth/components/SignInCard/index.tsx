import { observer } from 'mobx-react-lite';
import { withContextProps } from 'react-props-from-context';
import { useMessages } from './useMessages';
import { AuthCard, AuthCardS } from '/src/auth/components/AuthCard';
import { SignInForm } from '/src/auth/components/SignInForm';
import { useSignIn } from '/src/auth/endpoints';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { useResetAuthState } from '/src/auth/hooks/useResetAuthState';
import { authNav } from '/src/auth/routes';
import { L } from '/src/frames/layout';
import { history } from '/src/routes/history';
import { navTo } from '/src/routes/navHandler';
import { cn } from '/src/utils/classnames';
import { useSearchAndUrlParams } from '/src/utils/hooks/useSearchAndUrlParams';
import { ObjT } from '/src/utils/types';

// Import styles
import './index.scss';

export type PropsT = {};

const ContextProps = {
  authState: authStateCtx.authState,
};

export const SignInCard = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    useResetAuthState(props.authState);
    const { messages } = useMessages();
    const signIn = useSignIn(props.authState).mutateAsync;
    const params = useSearchAndUrlParams();

    return (
      //
      // 🔳 SignInCard 🔳
      //
      <AuthCard id="SignInCard">
        {
          // 🔳 SignInForm 🔳
        }
        <SignInForm
          className={cn(AuthCardS.Form())}
          signIn={(email: string, password: string) => {
            return signIn({ userId: email, password }).then(
              (response: ObjT) => {
                if (props.authState.isAuthenticated) {
                  const routeSpec = params.nextUrl
                    ? { url: params.nextUrl, nav: history.push }
                    : authNav.home({});
                  navTo(routeSpec);
                }
              }
            );
          }}
          errors={props.authState.errors}
        />

        {
          // 🔳 Changed your mind message 🔳
        }
        <div
          className={cn(
            AuthCardS.FormCaption(),
            'SignInCard__ChangedYourMind',
            [L.col.banner()]
          )}
        >
          {messages.divChangedYourMind}
        </div>
      </AuthCard>
    );
  }, ContextProps)
);
