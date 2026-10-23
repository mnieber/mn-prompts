import { http, HttpResponse } from 'msw';
import { getBlogPostsUrl } from '/src/api/queries/useGetBlogPosts';
import { hostUrl } from '/src/api/restClient';
import { createBlogPost } from '/src/api/types/BlogPostT';
import { joinUrls } from '/src/utils/urls';

export const handleGetBlogPosts = http.get(
  joinUrls(hostUrl, getBlogPostsUrl),
  () => {
    return HttpResponse.json([
      createBlogPost({
        title: 'First Post',
        slug: 'first-post',
        content: 'One',
      }),
      createBlogPost({
        title: 'Second Post',
        slug: 'second-post',
        content: 'Two',
      }),
    ]);
  }
);
