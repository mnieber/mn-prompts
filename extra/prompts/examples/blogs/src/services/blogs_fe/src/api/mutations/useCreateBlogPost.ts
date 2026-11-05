import snakecaseKeys from 'snakecase-keys';
import { z } from 'zod';
import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { post } from '/src/api/restClient';
import {
  BlogPostLevelSchema,
  BlogPostSchema,
} from '/src/api/types/BlogPostSchema';
import { BlogPostT } from '/src/api/types/BlogPostT';
import { BlogT } from '/src/api/types/BlogT';
import { parseResponse } from '/src/api/utils/parseResponse';
import { noFields, requestFailure } from '/src/api/utils/requestFailure';
import { ok, ResultT, UnexpectedErrorT } from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

export const CreateBlogPostFormSchema = z.object({
  title: z.string(),
  content: z.string().nullish(),
  level: BlogPostLevelSchema,
});

export type CreateBlogPostArgsT = {
  blog: BlogT;
  createBlogPostForm: z.input<typeof CreateBlogPostFormSchema>;
};

export type CreateBlogPostResultT = ResultT<BlogPostT, CreateBlogPostErrorT>;
export type CreateBlogPostErrorT =
  | { code: 'BLOG_POST_TITLE_ALREADY_EXISTS' }
  | { code: 'FORM_CONTAINS_FORBIDDEN_WORDS'; fieldName: string }
  | UnexpectedErrorT;

export const createBlogPost = (
  args: CreateBlogPostArgsT
): Promise<CreateBlogPostResultT> => {
  const url = `/blogs/${args.blog.id}/blog-posts/create/`;
  const createBlogPostForm = CreateBlogPostFormSchema.parse(
    args.createBlogPostForm
  );
  return post(url, {
    create_blog_post_form: snakecaseKeys(createBlogPostForm),
    blog_id: args.blog.id,
  }).then(
    (response) =>
      waitOnDev(1000, ok(parseResponse(BlogPostSchema, response.data))),
    (error) =>
      waitOnDev(
        1000,
        requestFailure(error, {
          BLOG_POST_TITLE_ALREADY_EXISTS: noFields,
          FORM_CONTAINS_FORBIDDEN_WORDS: (details) => ({ fieldName: details }),
        })
      )
  );
};

export const useCreateBlogPost = () => {
  return useObservableMutation({
    mutationFn: createBlogPost,
    onSuccess: (result, args) => {
      if (result.ok) {
        invalidateGetBlogPosts({ blogSlug: args.blog.slug });
      }
    },
  });
};
