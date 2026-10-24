import { createBlog } from '/tests/fakeBackend/endpoints/createBlog';
import { createBlogPost } from '/tests/fakeBackend/endpoints/createBlogPost';
import { deleteBlogPosts } from '/tests/fakeBackend/endpoints/deleteBlogPosts';
import { getBlogPosts } from '/tests/fakeBackend/endpoints/getBlogPosts';
import { getBlogs } from '/tests/fakeBackend/endpoints/getBlogs';
import { getBlogTags } from '/tests/fakeBackend/endpoints/getBlogTags';
import { loadUserId } from '/tests/fakeBackend/endpoints/loadUserId';
import { updateBlogPost } from '/tests/fakeBackend/endpoints/updateBlogPost';

export const endpoints = [
  loadUserId,
  getBlogs,
  getBlogPosts,
  getBlogTags,
  createBlog,
  createBlogPost,
  updateBlogPost,
  deleteBlogPosts,
];
