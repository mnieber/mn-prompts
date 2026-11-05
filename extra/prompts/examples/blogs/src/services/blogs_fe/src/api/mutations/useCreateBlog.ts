import snakecaseKeys from 'snakecase-keys';
import { z } from 'zod';
import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogs } from '/src/api/queries/useGetBlogs';
import { post } from '/src/api/restClient';
import { BlogSchema } from '/src/api/types/BlogSchema';
import { BlogT } from '/src/api/types/BlogT';
import { parseResponse } from '/src/api/utils/parseResponse';
import { noFields, requestFailure } from '/src/api/utils/requestFailure';
import { ok, ResultT, UnexpectedErrorT } from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

export const CreateBlogFormSchema = z.object({
  name: z.string(),
  description: z.string().nullish(),
});

export type CreateBlogArgsT = {
  createBlogForm: z.input<typeof CreateBlogFormSchema>;
};

export type CreateBlogErrorT =
  | { code: 'BLOG_NAME_ALREADY_EXISTS' }
  | { code: 'FORM_CONTAINS_FORBIDDEN_WORDS'; fieldName: string }
  | UnexpectedErrorT;
export type CreateBlogResultT = ResultT<BlogT, CreateBlogErrorT>;

export const createBlog = (
  args: CreateBlogArgsT
): Promise<CreateBlogResultT> => {
  const url = `/blogs/create/`;
  const createBlogForm = CreateBlogFormSchema.parse(args.createBlogForm);
  return post(url, {
    create_blog_form: snakecaseKeys(createBlogForm),
  }).then(
    (response) => waitOnDev(1000, ok(parseResponse(BlogSchema, response.data))),
    (error) =>
      waitOnDev(
        1000,
        requestFailure(error, {
          BLOG_NAME_ALREADY_EXISTS: noFields,
          FORM_CONTAINS_FORBIDDEN_WORDS: (details) => ({ fieldName: details }),
        })
      )
  );
};

export const useCreateBlog = () => {
  return useObservableMutation({
    mutationFn: createBlog,
    onSuccess: (result) => {
      if (result.ok) {
        invalidateGetBlogs({});
      }
    },
  });
};
