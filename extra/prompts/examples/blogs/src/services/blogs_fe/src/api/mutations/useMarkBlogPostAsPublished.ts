import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { post } from '/src/api/restClient';
import { BlogT } from '/src/api/types/BlogT';
import { waitOnDev } from '/src/utils/wait';

export type MarkBlogPostAsPublishedArgsT = {
  blog: BlogT;
  blogPostId: string;
};

export const markBlogPostAsPublished = (args: MarkBlogPostAsPublishedArgsT) => {
  const url = `/blogs/${args.blog.id}/blog-posts/${args.blogPostId}/publish/`;
  return post(url, {})
    .then((response) => {
      return waitOnDev(1000, response);
    })
    .catch((error) => {
      // Handle specific error cases if needed
      throw error;
    });
};

export const useMarkBlogPostAsPublished = () => {
  return useObservableMutation({
    mutationFn: markBlogPostAsPublished,
    onSuccess: (response: any, args: MarkBlogPostAsPublishedArgsT) => {
      invalidateGetBlogPosts({ blogSlug: args.blog.slug });
    },
  });
};
