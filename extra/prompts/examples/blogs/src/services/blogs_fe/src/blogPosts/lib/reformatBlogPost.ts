import { BlogPostT } from '/src/api/types';

export function reformatBlogPost(blogPost: BlogPostT): BlogPostT {
  return {
    ...blogPost,
    title: blogPost.title.trim(),
    content: (blogPost.content ?? '').trim(),
  };
}
