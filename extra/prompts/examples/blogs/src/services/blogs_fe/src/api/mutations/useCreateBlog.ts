import snakecaseKeys from 'snakecase-keys';
import { z } from 'zod';
import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogs } from '/src/api/queries/useGetBlogs';
import { post } from '/src/api/restClient';
import { BlogSchema } from '/src/api/types/BlogSchema';
import { parseResponse } from '/src/api/utils/parseResponse';
import { hasErrorCode } from '/src/auth/utils/hasErrorCode';
import { ObjT } from '/src/utils/types';
import { waitOnDev } from '/src/utils/wait';

export const CreateBlogFormSchema = z.object({
  name: z.string(),
  slug: z.string(),
  description: z.string().nullish(),
});

export type CreateBlogArgsT = {
  createBlogForm: z.input<typeof CreateBlogFormSchema>;
};

export const createBlog = (args: CreateBlogArgsT) => {
  const url = `/blogs/create/`;
  const createBlogForm = CreateBlogFormSchema.parse(args.createBlogForm);
  return post(url, {
    create_blog_form: snakecaseKeys(createBlogForm),
  })
    .then((response) => {
      const res = parseResponse(BlogSchema, response.data);

      return waitOnDev(1000, res);
    })
    .catch((error) => {
      if (hasErrorCode(error.response.data, ['BLOG_NAME_ALREADY_EXISTS'])) {
        return waitOnDev(1000, {
          success: false,
          errorCode: 'BLOG_NAME_ALREADY_EXISTS',
        });
      }

      throw error;
    });
};

export const useCreateBlog = () => {
  return useObservableMutation({
    mutationFn: createBlog,
    onSuccess: (response: ObjT, args: CreateBlogArgsT) => {
      invalidateGetBlogs({});
    },
  });
};
