import { createBlog } from '/tests/testEnv/endpoints/createBlog';
import { getBlogPosts } from '/tests/testEnv/endpoints/getBlogPosts';
import { getBlogs } from '/tests/testEnv/endpoints/getBlogs';
import { loadUserId } from '/tests/testEnv/endpoints/loadUserId';

export const endpoints = [loadUserId, getBlogs, getBlogPosts, createBlog];
