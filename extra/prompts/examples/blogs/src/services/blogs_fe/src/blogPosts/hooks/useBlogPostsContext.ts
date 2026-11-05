import * as R from 'ramda';
import React from 'react';
import { Addition, Highlight } from 'skandha-facets';
import { BlogPostT } from '/src/api/types';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';
import { BlogPostsDeletion } from '/src/blogPosts/BlogPostsState/facets/BlogPostsDeletion';
import { BlogPostsEdit } from '/src/blogPosts/BlogPostsState/facets/BlogPostsEdit';
import { BlogPostsSelection } from '/src/blogPosts/BlogPostsState/facets/BlogPostsSelection';

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
    ] as any as BlogPostsDeletion,
    blogPostsEdit: [
      useBlogPostsContext,
      'blogPostsEdit',
    ] as any as BlogPostsEdit,
    blogPostsHighlight: [
      useBlogPostsContext,
      'blogPostsHighlight',
    ] as any as Highlight,
    blogPostsSelection: [
      useBlogPostsContext,
      'blogPostsSelection',
    ] as any as BlogPostsSelection,
  },
]);
