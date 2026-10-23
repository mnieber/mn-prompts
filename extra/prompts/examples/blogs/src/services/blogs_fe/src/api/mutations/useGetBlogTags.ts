import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { get } from '/src/api/restClient';
import { createQueryKey } from '/src/api/utils/createQueryKey';
import { waitOnDev } from '/src/utils/wait';

export type GetBlogTagsArgsT = {
  inputValue: string;
};

export type QueryKeyT = GetBlogTagsArgsT;
export function getBlogTagsQueryKey(args: QueryKeyT) {
  return createQueryKey<QueryKeyT>('getBlogTags', args);
}

export const getBlogTagsUrl = '/blogs/tags/';

export const getBlogTags = (args: GetBlogTagsArgsT) => {
  return get(`${getBlogTagsUrl}?input_value=${args.inputValue}`).then(
    (response) => {
      return waitOnDev(1000, response.data);
    }
  );
};

export const useGetBlogTags = () => {
  return useObservableMutation({
    mutationFn: getBlogTags,
  });
};
