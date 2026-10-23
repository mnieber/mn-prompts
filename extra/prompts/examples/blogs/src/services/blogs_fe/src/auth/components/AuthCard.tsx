import { observer } from 'mobx-react-lite';
import React from 'react';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './AuthCard.scss';

type PropsT = React.PropsWithChildren<{
  id: string;
}>;

export const AuthCard = observer((props: PropsT) => {
  return (
    <div className={cn('AuthCard', ['w-[396px]'])}>
      <div
        id={props.id}
        className={cn('AuthCard__Inner', [L.col.banner(), 'px-8 py-6'])}
      >
        {props.children}
      </div>
    </div>
  );
});

// An AuthCard has:
// - a Form
// - a FormCaption that appears just below the form (e.g. "Did you forget your password?")
// - a CardFooter that appears at the bottom of the card (e.g. "Register for an account")
export const AuthCardS = {
  Form: () => '',
  FormCaption: () => 'mt-2',
  CardFooter: () => 'mt-8',
};
