import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import {
  getBlogPostsQueryKey,
  invalidateGetBlogPosts,
} from '/src/api/queries/useGetBlogPosts';
import { queryClient } from '/src/api/queryClient';
import { post } from '/src/api/restClient';
import { BlogT } from '/src/api/types/BlogT';
import { ObjT } from '/src/utils/types';
import { waitOnDev } from '/src/utils/wait';

export type DeleteBlogPostsArgsT = {
  blog: BlogT;
  blogPostIds: string[];
};

export const deleteBlogPosts = (args: DeleteBlogPostsArgsT) => {
  const url = `/blogs/${args.blog.id}/blog-posts/delete/`;
  return post(url, {
    delete_blog_posts_form: {
      blog_post_ids: args.blogPostIds,
    },
  })
    .then((response) => {
      return waitOnDev(1000, response);
    })
    .catch((error) => {
      const errorCodes = error.response.data;
      if (errorCodes.includes('BLOG_POSTS_NOT_FOUND')) {
        return waitOnDev(1000, {
          success: false,
        });
      }

      throw error;
    });
};

export const useDeleteBlogPosts = () => {
  return useObservableMutation({
    mutationFn: deleteBlogPosts,
    onSuccess: (response: ObjT, args: DeleteBlogPostsArgsT) => {
      invalidateGetBlogPosts({ blogSlug: args.blog.slug });
      queryClient.setQueryData(
        getBlogPostsQueryKey({ blogSlug: args.blog.slug }),
        (data: any) => {
          return {
            blogPosts: data.blogPosts.filter(
              (x: any) => !args.blogPostIds.includes(x.id)
            ),
          };
        }
      );
    },
  });
};
