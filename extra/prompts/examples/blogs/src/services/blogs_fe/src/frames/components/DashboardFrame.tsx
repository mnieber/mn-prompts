import React from 'react';
import { CreateBlogButton } from '/src/blogPosts/components/CreateBlogButton';
import { AccountMenu } from '/src/frames/components/AccountMenu';
import { ErrorBanner } from '/src/frames/components/ErrorBanner';
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
      <div className={cn('DashboardFrame__TopBar')}>
        <div className={cn('DashboardFrame__TopBarInner', L.row.skewer())}>
          <div className={cn('DashboardFrame__Brand')}>
            Blog<span className="text-accent">Manager</span>
          </div>
          <CreateBlogButton className="ml-auto mr-2" />
          <AccountMenu />
        </div>
      </div>
      <ErrorBanner />
      {props.children}
    </div>
  );
};

export const DashboardFrameS = {};
