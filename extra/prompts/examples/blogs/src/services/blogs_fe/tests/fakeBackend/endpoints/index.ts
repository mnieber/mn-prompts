import { createBlog } from '/tests/fakeBackend/endpoints/createBlog';
import { getBlogPosts } from '/tests/fakeBackend/endpoints/getBlogPosts';
import { getBlogs } from '/tests/fakeBackend/endpoints/getBlogs';
import { loadUserId } from '/tests/fakeBackend/endpoints/loadUserId';

export const endpoints = [loadUserId, getBlogs, getBlogPosts, createBlog];
