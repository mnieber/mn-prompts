import { observer } from 'mobx-react-lite';
import { withContextProps } from 'react-props-from-context';
import { Route, Switch } from 'wouter';
import { SignInPage } from '/src/auth/components/SignInPage';
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
      </Switch>
    );
  }, ContextProps)
);
