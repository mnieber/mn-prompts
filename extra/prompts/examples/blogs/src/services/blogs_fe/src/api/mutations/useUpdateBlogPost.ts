import snakecaseKeys from 'snakecase-keys';
import { z } from 'zod';
import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { post } from '/src/api/restClient';
import { BlogPostT } from '/src/api/types';
import { CreateBlogPostFormSchema } from '/src/api/mutations/useCreateBlogPost';
import { BlogPostSchema } from '/src/api/types/BlogPostSchema';
import { BlogT } from '/src/api/types/BlogT';
import { parseResponse } from '/src/api/utils/parseResponse';
import { noFields, requestFailure } from '/src/api/utils/requestFailure';
import { ok, ResultT, UnexpectedErrorT } from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

// The fields that we send (each one is optional). Parsing the form with this schema
// drops the other fields (e.g. isTransient).
export const UpdateBlogPostFormSchema = CreateBlogPostFormSchema.partial();

export type UpdateBlogPostArgsT = {
  blog: BlogT;
  blogPost: BlogPostT;
  updateBlogPostForm: z.input<typeof UpdateBlogPostFormSchema>;
};

export type UpdateBlogPostResultT = ResultT<BlogPostT, UpdateBlogPostErrorT>;
export type UpdateBlogPostErrorT =
  | { code: 'BLOG_POST_TITLE_ALREADY_EXISTS' }
  | { code: 'BLOG_POST_NOT_FOUND' }
  | { code: 'FORM_CONTAINS_FORBIDDEN_WORDS'; fieldName: string }
  | UnexpectedErrorT;

export const updateBlogPost = (
  args: UpdateBlogPostArgsT
): Promise<UpdateBlogPostResultT> => {
  const url = `/blogs/${args.blog.id}/blog-posts/${args.blogPost.id}/update/`;
  const updateBlogPostForm = UpdateBlogPostFormSchema.parse(
    args.updateBlogPostForm
  );
  return post(url, {
    update_blog_post_form: snakecaseKeys(updateBlogPostForm),
    blog_id: args.blog.id,
    blog_post_id: args.blogPost.id,
  }).then(
    (response) =>
      waitOnDev(1000, ok(parseResponse(BlogPostSchema, response.data))),
    (error) =>
      waitOnDev(
        1000,
        requestFailure(error, {
          BLOG_POST_TITLE_ALREADY_EXISTS: noFields,
          BLOG_POST_NOT_FOUND: noFields,
          FORM_CONTAINS_FORBIDDEN_WORDS: (details) => ({ fieldName: details }),
        })
      )
  );
};

// Whether this failure means that our list of blog posts is stale.
const isListStale = (error: UpdateBlogPostErrorT): boolean => {
  switch (error.code) {
    case 'BLOG_POST_NOT_FOUND':
      return true;
    case 'BLOG_POST_TITLE_ALREADY_EXISTS':
    case 'FORM_CONTAINS_FORBIDDEN_WORDS':
    case 'UNEXPECTED':
      return false;
  }
};

export const useUpdateBlogPost = () => {
  return useObservableMutation({
    mutationFn: updateBlogPost,
    onSuccess: (result, args) => {
      if (result.ok || isListStale(result.error)) {
        invalidateGetBlogPosts({ blogSlug: args.blog.slug });
      }
    },
  });
};
