import React from 'react';
import { Link } from 'wouter';
import { cn } from '/src/utils/classnames';

type PropsT = React.PropsWithChildren<{
  to: string;
  className?: any;
  dataCy?: string;
  onClick?: (event: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void;
}>;

export const RouterLink = (props: PropsT) => {
  return (
    <Link
      data-cy={props.dataCy}
      className={cn(props.className)}
      to={props.to}
      onClick={props.onClick}
    >
      {props.children as any}
    </Link>
  );
};
