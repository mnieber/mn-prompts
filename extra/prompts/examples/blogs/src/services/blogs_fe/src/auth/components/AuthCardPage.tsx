import React from 'react';
import { AuthPage, AuthPageS } from '/src/auth/components/AuthPage';
import { SignInLogo } from '/src/frames/components/SignInLogo';
import { cn } from '/src/utils/classnames';

type PropsT = React.PropsWithChildren<{}>;

// The page of an auth flow: the logo, and the card of the flow.
export const AuthCardPage = (props: PropsT) => {
  return (
    <AuthPage className="flex-grow">
      <SignInLogo />
      <div className={cn(AuthPageS.Gap())} />
      {props.children}
    </AuthPage>
  );
};
