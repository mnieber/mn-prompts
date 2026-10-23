import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';
import { queryClient } from '/src/api/queryClient';
import { get } from '/src/api/restClient';
import { BlogPostSchema } from '/src/api/types/BlogPostSchema';
import { createQueryKey } from '/src/api/utils/createQueryKey';
import { parseResponse } from '/src/api/utils/parseResponse';
import { generatePath } from '/src/routes/utils';
import { waitOnDev } from '/src/utils/wait';

export type GetBlogPostsArgsT = {
  blogSlug: string;
};
export type OptionsT = {
  enabled?: boolean;
};

export type GetBlogPostsQueryKeyT = GetBlogPostsArgsT;
export function getBlogPostsQueryKey(args: GetBlogPostsQueryKeyT) {
  return createQueryKey<GetBlogPostsQueryKeyT>('getBlogPosts', args);
}

export const getBlogPostsUrl = '/blogs/:blogSlug/blog-posts/list/';

export const getBlogPosts = (args: GetBlogPostsArgsT) => {
  return get(generatePath(getBlogPostsUrl, { blogSlug: args.blogSlug })).then(
    (response) => {
      const res = parseResponse(z.array(BlogPostSchema), response.data);

      return waitOnDev(100, { blogPosts: res });
    }
  );
};

export const useGetBlogPosts = (
  args: GetBlogPostsArgsT,
  options?: OptionsT
) => {
  return useQuery({
    queryKey: getBlogPostsQueryKey(args),
    queryFn: () => getBlogPosts(args),
    enabled: !!(options?.enabled ?? true),
  });
};

export const invalidateGetBlogPosts = (args: GetBlogPostsQueryKeyT) => {
  return queryClient.invalidateQueries({
    queryKey: getBlogPostsQueryKey(args),
  });
};
