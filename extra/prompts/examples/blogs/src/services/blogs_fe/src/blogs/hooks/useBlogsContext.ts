import * as R from 'ramda';
import React from 'react';
import { Addition, Edit, Highlight, Selection } from 'skandha-facets';
import { BlogT } from '/src/api/types';
import { BlogsState } from '/src/blogs/BlogsState';

export const BlogsContext = React.createContext<any>(null);

export const useBlogsContext = () => {
  const context = React.useContext(BlogsContext);
  if (!context) {
    throw new Error(
      'useBlogsContext must be used within a BlogsContext.Provider'
    );
  }
  return context;
};

export const blogsCtx = R.mergeAll([
  {
    blogsState: [useBlogsContext, 'blogsState'] as any as BlogsState,
    blogs: [useBlogsContext, 'blogs'] as any as BlogT[],
    blog: [useBlogsContext, 'blog'] as any as BlogT,
    blogsHighlight: [useBlogsContext, 'blogsHighlight'] as any as Highlight,
    blogsSelection: [useBlogsContext, 'blogsSelection'] as any as Selection,
    blogsAddition: [useBlogsContext, 'blogsAddition'] as any as Addition,
    blogsEdit: [useBlogsContext, 'blogsEdit'] as any as Edit,
  },
]);
