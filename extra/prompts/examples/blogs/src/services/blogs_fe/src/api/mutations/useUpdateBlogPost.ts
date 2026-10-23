import snakecaseKeys from 'snakecase-keys';
import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { post } from '/src/api/restClient';
import { BlogPostT } from '/src/api/types';
import { BlogPostSchema } from '/src/api/types/BlogPostSchema';
import { BlogT } from '/src/api/types/BlogT';
import { parseResponse } from '/src/api/utils/parseResponse';
import { ObjT } from '/src/utils/types';
import { waitOnDev } from '/src/utils/wait';

export type UpdateBlogPostArgsT = {
  blog: BlogT;
  blogPost: BlogPostT;
  updateBlogPostForm: {
    title?: string;
    content?: string;
  };
};

export const updateBlogPost = (args: UpdateBlogPostArgsT) => {
  const url = `/blogs/${args.blog.id}/blog-posts/${args.blogPost.id}/update/`;
  return post(url, {
    update_blog_post_form: snakecaseKeys(args.updateBlogPostForm),
    blog_id: args.blog.id,
    blog_post_id: args.blogPost.id,
  })
    .then((response) => {
      const res = parseResponse(BlogPostSchema, response);

      return waitOnDev(1000, res);
    })
    .catch((error) => {
      const errorCodes = error.response.data;
      if (errorCodes.includes('BLOG_NOT_FOUND')) {
        // TODO return this error and use it in UpdateBlogPostForm
        return waitOnDev(1000, {
          success: false,
        });
      }
      if (errorCodes.includes('BLOG_POST_NOT_FOUND')) {
        // TODO return this error and use it in UpdateBlogPostForm
        return waitOnDev(1000, {
          success: false,
        });
      }

      throw error;
    });
};

export const useUpdateBlogPost = () => {
  return useObservableMutation({
    mutationFn: updateBlogPost,
    onSuccess: (response: ObjT, args: UpdateBlogPostArgsT) => {
      invalidateGetBlogPosts({ blogSlug: args.blog.slug });
    },
  });
};
