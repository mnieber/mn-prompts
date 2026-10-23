import React from 'react';
import { CreateBlogButton } from '/src/blogPosts/components/CreateBlogButton';
import { AccountMenu } from '/src/frames/components/AccountMenu';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './DashboardFrame.scss';

type PropsT = React.PropsWithChildren<{
  className?: any;
}>;

export const DashboardFrame = (props: PropsT) => {
  return (
    <div className={cn('DashboardFrame', L.col.banner(), props.className)}>
      <div className={cn('DashboardFrame__TopBar', L.row.bar())}>
        <CreateBlogButton />
        <AccountMenu />
      </div>
      {props.children}
    </div>
  );
};

export const DashboardFrameS = {};
