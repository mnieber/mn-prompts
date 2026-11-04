import snakecaseKeys from 'snakecase-keys';
import { z } from 'zod';
import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { post } from '/src/api/restClient';
import {
  BlogPostLevelSchema,
  BlogPostSchema,
} from '/src/api/types/BlogPostSchema';
import { BlogT } from '/src/api/types/BlogT';
import { isFailedMutation } from '/src/api/utils/isFailedMutation';
import { parseResponse } from '/src/api/utils/parseResponse';
import { getErrorDetail } from '/src/auth/utils/getErrorDetail';
import { hasErrorCode } from '/src/auth/utils/hasErrorCode';
import { ObjT } from '/src/utils/types';
import { waitOnDev } from '/src/utils/wait';

export const CreateBlogPostFormSchema = z.object({
  title: z.string(),
  slug: z.string(),
  content: z.string().nullish(),
  level: BlogPostLevelSchema,
  tags: z.array(z.string()).nullish(),
});

export type CreateBlogPostArgsT = {
  blog: BlogT;
  createBlogPostForm: z.input<typeof CreateBlogPostFormSchema>;
};

export const createBlogPost = (args: CreateBlogPostArgsT) => {
  const url = `/blogs/${args.blog.id}/blog-posts/create/`;
  const createBlogPostForm = CreateBlogPostFormSchema.parse(
    args.createBlogPostForm
  );
  return post(url, {
    create_blog_post_form: snakecaseKeys(createBlogPostForm),
    blog_id: args.blog.id,
  })
    .then((response) => {
      const res = parseResponse(BlogPostSchema, response.data);

      return waitOnDev(1000, res);
    })
    .catch((error) => {
      if (
        hasErrorCode(error.response.data, ['BLOG_POST_TITLE_ALREADY_EXISTS'])
      ) {
        return waitOnDev(1000, {
          success: false,
          errorCode: 'BLOG_POST_TITLE_ALREADY_EXISTS',
        });
      }
      if (
        hasErrorCode(error.response.data, ['FORM_CONTAINS_FORBIDDEN_WORDS'])
      ) {
        return waitOnDev(1000, {
          success: false,
          errorCode: 'FORM_CONTAINS_FORBIDDEN_WORDS',
          // The backend names the field that contains the forbidden words
          fieldName: getErrorDetail(
            error.response.data,
            'FORM_CONTAINS_FORBIDDEN_WORDS'
          ),
        });
      }
      if (hasErrorCode(error.response.data, ['BLOG_NOT_FOUND'])) {
        return waitOnDev(1000, {
          success: false,
        });
      }

      throw error;
    });
};

export const useCreateBlogPost = () => {
  return useObservableMutation({
    mutationFn: createBlogPost,
    onSuccess: (response: ObjT, args: CreateBlogPostArgsT) => {
      if (isFailedMutation(response)) {
        return;
      }
      invalidateGetBlogPosts({ blogSlug: args.blog.slug });
    },
  });
};
