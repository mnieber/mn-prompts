import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import {
  getBlogPostsQueryKey,
  invalidateGetBlogPosts,
} from '/src/api/queries/useGetBlogPosts';
import { queryClient } from '/src/api/queryClient';
import { post } from '/src/api/restClient';
import { BlogT } from '/src/api/types/BlogT';
import { noFields, requestFailure } from '/src/api/utils/requestFailure';
import { ok, ResultT, UnexpectedErrorT } from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

export type DeleteBlogPostsArgsT = {
  blog: BlogT;
  blogPostIds: string[];
};

export type DeleteBlogPostsResultT = ResultT<void, DeleteBlogPostsErrorT>;
export type DeleteBlogPostsErrorT =
  | { code: 'BLOG_POSTS_NOT_FOUND' }
  | UnexpectedErrorT;

export const deleteBlogPosts = (
  args: DeleteBlogPostsArgsT
): Promise<DeleteBlogPostsResultT> => {
  const url = `/blogs/${args.blog.id}/blog-posts/delete/`;
  return post(url, {
    delete_blog_posts_form: {
      blog_post_ids: args.blogPostIds,
    },
  }).then(
    () => waitOnDev(1000, ok()),
    (error) =>
      waitOnDev(
        1000,
        requestFailure(error, {
          //
          BLOG_POSTS_NOT_FOUND: noFields,
        })
      )
  );
};

export const useDeleteBlogPosts = () => {
  return useObservableMutation({
    mutationFn: deleteBlogPosts,
    onSuccess: (result, args) => {
      // After a failure our list may be stale, so refresh it in both cases
      invalidateGetBlogPosts({ blogSlug: args.blog.slug });
      if (!result.ok) {
        return;
      }
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
