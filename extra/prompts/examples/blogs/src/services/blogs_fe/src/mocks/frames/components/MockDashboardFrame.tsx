import React from 'react';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './MockDashboardFrame.scss';

type PropsT = React.PropsWithChildren<{
  className?: any;
}>;

export const MockDashboardFrame = (props: PropsT) => {
  return (
    <div className={cn('MockDashboardFrame', L.col.banner(), props.className)}>
      {props.children}
    </div>
  );
};

export const DashboardFrameS = {};
