import classnames from 'classnames';
import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import React from 'react';
import { Link } from 'wouter';
import './BlogListViewItem.scss';
import { BlogT } from '/src/api/types';

export type PropsT = {
  blog: BlogT;
  url: string;
  isInert?: boolean;
  className?: any;
};

export const BlogListViewItem: React.FC<PropsT> = observer((props: PropsT) => {
  return (
    <Link
      href={props.url}
      onClick={(e: React.MouseEvent) => {
        if (props.isInert) {
          e.preventDefault();
        }
      }}
      className={classnames(
        'BlogListViewItem',
        { 'animate-delete': isUpdating(props.blog) },
        props.className
      )}
    >
      {props.blog.name}
    </Link>
  );
});
