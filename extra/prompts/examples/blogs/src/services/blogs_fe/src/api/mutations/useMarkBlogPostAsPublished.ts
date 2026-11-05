import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { post } from '/src/api/restClient';
import { BlogT } from '/src/api/types/BlogT';
import {
  ok,
  ResultT,
  unexpectedErr,
  UnexpectedErrorT,
} from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

export type MarkBlogPostAsPublishedArgsT = {
  blog: BlogT;
  blogPostId: string;
};

export type MarkBlogPostAsPublishedErrorT = UnexpectedErrorT;
export type MarkBlogPostAsPublishedResultT = ResultT<
  void,
  MarkBlogPostAsPublishedErrorT
>;

export const markBlogPostAsPublished = (
  args: MarkBlogPostAsPublishedArgsT
): Promise<MarkBlogPostAsPublishedResultT> => {
  const url = `/blogs/${args.blog.id}/blog-posts/${args.blogPostId}/publish/`;
  return post(url, {}).then(
    () => waitOnDev(1000, ok()),
    (error) => waitOnDev(1000, unexpectedErr(error))
  );
};

export const useMarkBlogPostAsPublished = () => {
  return useObservableMutation({
    mutationFn: markBlogPostAsPublished,
    onSuccess: (result, args) => {
      if (result.ok) {
        invalidateGetBlogPosts({ blogSlug: args.blog.slug });
      }
    },
  });
};
