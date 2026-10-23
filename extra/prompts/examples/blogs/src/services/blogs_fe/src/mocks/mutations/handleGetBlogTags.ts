import { http, HttpResponse } from 'msw';
import { getBlogTagsUrl } from '/src/api/mutations/useGetBlogTags';
import { hostUrl } from '/src/api/restClient';

export const handleGetBlogTags = http.post(
  `${hostUrl}${getBlogTagsUrl}*`,
  () => {
    return HttpResponse.json({
      tags: ['sports', 'music'],
    });
  }
);
