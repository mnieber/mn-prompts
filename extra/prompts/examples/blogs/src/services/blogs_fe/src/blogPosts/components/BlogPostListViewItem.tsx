import classnames from 'classnames';
import mergeProps from 'merge-props';
import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import React from 'react';
import { selectionUIHandlers, SelectionUIPropsT } from 'skandha-facets';
import './BlogPostListViewItem.scss';
import { BlogPostT } from '/src/api/types';
import { BlogT } from '/src/api/types/BlogT';
import { blogPostsNav } from '/src/blogPosts/routes';
import { navTo } from '/src/routes/navHandler';

export type PropsT = {
  blog: BlogT;
  blogPost: BlogPostT;
  className?: any;
  selectionUIProps: SelectionUIPropsT;
};

export const BlogPostListViewItem: React.FC<PropsT> = observer(
  (props: PropsT) => {
    return (
      <div
        className={classnames(
          'BlogPostListViewItem',
          { 'animate-delete': isUpdating(props.blogPost) },
          props.className
        )}
        {...mergeProps(selectionUIHandlers(props.selectionUIProps), {
          onClick: (e: React.MouseEvent<HTMLDivElement>) => {
            if (!(e.ctrlKey || e.shiftKey)) {
              navTo(
                blogPostsNav.blogPost({
                  blogSlug: props.blog.slug,
                  blogPostSlug: props.blogPost.slug,
                })
              );
            }
          },
        })}
      >
        {props.blogPost.title}
        {props.blogPost.isPublished ? ' ✔️' : ''}
      </div>
    );
  }
);
