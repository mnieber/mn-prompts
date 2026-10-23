import { http, HttpResponse } from 'msw';
import { getBlogsUrl } from '/src/api/queries/useGetBlogs';
import { hostUrl } from '/src/api/restClient';
import { createBlog } from '/src/api/types/BlogT';
import { joinUrls } from '/src/utils/urls';

export const handleGetBlogs = http.get(joinUrls(hostUrl, getBlogsUrl), () => {
  return HttpResponse.json([
    createBlog({
      name: 'Judo',
      slug: 'judo',
    }),
    createBlog({
      name: 'Karate',
      slug: 'karate',
    }),
  ]);
});
