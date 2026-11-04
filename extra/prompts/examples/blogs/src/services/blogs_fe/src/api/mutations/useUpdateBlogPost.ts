import snakecaseKeys from 'snakecase-keys';
import { z } from 'zod';
import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { post } from '/src/api/restClient';
import { BlogPostT } from '/src/api/types';
import { CreateBlogPostFormSchema } from '/src/api/mutations/useCreateBlogPost';
import { BlogPostSchema } from '/src/api/types/BlogPostSchema';
import { BlogT } from '/src/api/types/BlogT';
import { isFailedMutation } from '/src/api/utils/isFailedMutation';
import { parseResponse } from '/src/api/utils/parseResponse';
import { getErrorDetail } from '/src/auth/utils/getErrorDetail';
import { hasErrorCode } from '/src/auth/utils/hasErrorCode';
import { ObjT } from '/src/utils/types';
import { waitOnDev } from '/src/utils/wait';

// The fields that we send (each one is optional). Parsing the form with this schema
// drops the other fields (e.g. isTransient).
export const UpdateBlogPostFormSchema = CreateBlogPostFormSchema.partial();

export type UpdateBlogPostArgsT = {
  blog: BlogT;
  blogPost: BlogPostT;
  updateBlogPostForm: z.input<typeof UpdateBlogPostFormSchema>;
};

export const updateBlogPost = (args: UpdateBlogPostArgsT) => {
  const url = `/blogs/${args.blog.id}/blog-posts/${args.blogPost.id}/update/`;
  const updateBlogPostForm = UpdateBlogPostFormSchema.parse(
    args.updateBlogPostForm
  );
  return post(url, {
    update_blog_post_form: snakecaseKeys(updateBlogPostForm),
    blog_id: args.blog.id,
    blog_post_id: args.blogPost.id,
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
        // TODO return this error and use it in UpdateBlogPostForm
        return waitOnDev(1000, {
          success: false,
        });
      }
      if (hasErrorCode(error.response.data, ['BLOG_POST_NOT_FOUND'])) {
        // TODO return this error and use it in UpdateBlogPostForm
        return waitOnDev(1000, {
          success: false,
        });
      }

      throw error;
    });
};

export const useUpdateBlogPost = () => {
  return useObservableMutation({
    mutationFn: updateBlogPost,
    onSuccess: (response: ObjT, args: UpdateBlogPostArgsT) => {
      if (isFailedMutation(response)) {
        return;
      }
      invalidateGetBlogPosts({ blogSlug: args.blog.slug });
    },
  });
};
