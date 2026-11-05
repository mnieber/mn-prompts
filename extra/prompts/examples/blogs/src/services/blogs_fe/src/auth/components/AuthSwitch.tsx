import { observer } from 'mobx-react-lite';
import { withContextProps } from 'react-props-from-context';
import { Route, Switch } from 'wouter';
import { AuthCardPage } from '/src/auth/components/AuthCardPage';
import { RequestPasswordResetCard } from '/src/auth/components/RequestPasswordResetCard';
import { ResetPasswordCard } from '/src/auth/components/ResetPasswordCard';
import { SignInPage } from '/src/auth/components/SignInPage';
import { SignUpCard } from '/src/auth/components/SignUpCard';
import { VerifyEmailCard } from '/src/auth/components/VerifyEmailCard';
import { authRoutes } from '/src/auth/routes';
import { blogsNav } from '/src/blogs/routes';
import { RedirectEffect } from '/src/routes/components';

type PropsT = {};

const ContextProps = {};

export const AuthSwitch = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    return (
      <Switch>
        <Route path={authRoutes.home()}>
          <RedirectEffect getRoute={() => blogsNav.blogs({})} />
        </Route>
        <Route path={authRoutes.signIn()}>
          <SignInPage />
        </Route>
        <Route path={authRoutes.signUp()}>
          <AuthCardPage>
            <SignUpCard />
          </AuthCardPage>
        </Route>
        <Route path={authRoutes.verifyEmail()}>
          <AuthCardPage>
            <VerifyEmailCard />
          </AuthCardPage>
        </Route>
        <Route path={authRoutes.requestPasswordReset()}>
          <AuthCardPage>
            <RequestPasswordResetCard />
          </AuthCardPage>
        </Route>
        <Route path={authRoutes.resetPassword()}>
          <AuthCardPage>
            <ResetPasswordCard />
          </AuthCardPage>
        </Route>
      </Switch>
    );
  }, ContextProps)
);
