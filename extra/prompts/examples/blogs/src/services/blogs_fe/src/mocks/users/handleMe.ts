import { http, HttpResponse } from 'msw';
import { hostUrl } from '/src/api/restClient';

export type HandleMeResponse = {
  data: string;
};

export const handleMe = http.get(`${hostUrl}/user/me/`, () => {
  return HttpResponse.json({
    data: 'fancy data string',
  } as HandleMeResponse);
});
