import * as R from 'ramda';
import React from 'react';
import { Addition, Deletion, Edit, Highlight, Selection } from 'skandha-facets';
import { BlogPostT } from '/src/api/types';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';
import { LoadValuePickerOptionsT } from '/src/utils/components/ValuePicker';

export const BlogPostsContext = React.createContext<any>(null);

export const useBlogPostsContext = () => {
  const context = React.useContext(BlogPostsContext);
  if (!context) {
    throw new Error(
      'useBlogPostsContext must be used within a BlogPostsContext.Provider'
    );
  }
  return context;
};

export const blogPostsCtx = R.mergeAll([
  {
    blogPostsState: [
      useBlogPostsContext,
      'blogPostsState',
    ] as any as BlogPostsState,
    blogPostsActions: [
      useBlogPostsContext,
      'blogPostsActions',
    ] as any as BlogPostsState['actionsCtr'],
    blogPost: [
      //
      useBlogPostsContext,
      'blogPost',
    ] as any as BlogPostT,
    blogPosts: [
      //
      useBlogPostsContext,
      'blogPosts',
    ] as any as BlogPostT[],
    blogPostsAddition: [
      useBlogPostsContext,
      'blogPostsAddition',
    ] as any as Addition,
    blogPostsDeletion: [
      useBlogPostsContext,
      'blogPostsDeletion',
    ] as any as Deletion,
    blogPostsEdit: [useBlogPostsContext, 'blogPostsEdit'] as any as Edit,
    blogPostsHighlight: [
      useBlogPostsContext,
      'blogPostsHighlight',
    ] as any as Highlight,
    blogPostsSelection: [
      useBlogPostsContext,
      'blogPostsSelection',
    ] as any as Selection,
    loadBlogTagsOptions: [
      useBlogPostsContext,
      'loadBlogTagsOptions',
    ] as any as LoadValuePickerOptionsT<any>,
  },
]);
