import React from 'react';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './AuthPage.scss';

type PropsT = React.PropsWithChildren<{
  className?: any;
}>;

export const AuthPage = (props: PropsT) => {
  return (
    <div className={cn('AuthPage', L.row.skewer(), props.className)}>
      {props.children}
    </div>
  );
};

// An AuthPage has:
// - a LogoCard that appears on the left.
// - a Gap that separates the LogoCard from the AuthCard.
// - an AuthCard on the right, e.g. a card for signing in.
export const AuthPageS = {
  Gap: () => 'AuthPage__Gap',
};
