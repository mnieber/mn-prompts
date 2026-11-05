import { createBlog } from '/tests/fakeBackend/endpoints/createBlog';
import { createBlogPost } from '/tests/fakeBackend/endpoints/createBlogPost';
import { deleteBlogPosts } from '/tests/fakeBackend/endpoints/deleteBlogPosts';
import { getBlogPosts } from '/tests/fakeBackend/endpoints/getBlogPosts';
import { getBlogs } from '/tests/fakeBackend/endpoints/getBlogs';
import { loadUserId } from '/tests/fakeBackend/endpoints/loadUserId';
import { markBlogPostAsPublished } from '/tests/fakeBackend/endpoints/markBlogPostAsPublished';
import { requestPasswordReset } from '/tests/fakeBackend/endpoints/requestPasswordReset';
import { resetPassword } from '/tests/fakeBackend/endpoints/resetPassword';
import { signInUser } from '/tests/fakeBackend/endpoints/signInUser';
import { signOut } from '/tests/fakeBackend/endpoints/signOut';
import { signUp } from '/tests/fakeBackend/endpoints/signUp';
import { updateBlogPost } from '/tests/fakeBackend/endpoints/updateBlogPost';
import { verifyEmail } from '/tests/fakeBackend/endpoints/verifyEmail';

export const endpoints = [
  loadUserId,
  getBlogs,
  getBlogPosts,
  createBlog,
  createBlogPost,
  updateBlogPost,
  deleteBlogPosts,
  markBlogPostAsPublished,
  signInUser,
  signOut,
  signUp,
  verifyEmail,
  requestPasswordReset,
  resetPassword,
];
