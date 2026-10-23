import { setupWorker } from 'msw/browser';
import { passthroughHandlers } from './defaultPassthrough';
import { handleGetBlogTags } from '/src/mocks/mutations/handleGetBlogTags';
import { handleGetBlogPosts } from '/src/mocks/queries/handleGetBlogPosts';
import { handleGetBlogs } from '/src/mocks/queries/handleGetBlogs';

export const handlers = [
  // Add more handlers here (but don't commit them to main)
  handleGetBlogs,
  handleGetBlogPosts,
  handleGetBlogTags,
  ...passthroughHandlers,
];

export const worker = setupWorker(...handlers);
