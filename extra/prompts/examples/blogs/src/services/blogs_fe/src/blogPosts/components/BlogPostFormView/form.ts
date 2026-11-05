import {
  FormState,
  HandleCancelArgsT,
  HandleSubmitArgsT,
  HandleValidateArgsT,
  unflatten,
} from 'react-form-state-context';
import { ContextProps, PropsT } from './index';
import { CreateBlogPostErrorT } from '/src/api/mutations/useCreateBlogPost';
import { UpdateBlogPostErrorT } from '/src/api/mutations/useUpdateBlogPost';
import { BlogPostT } from '/src/api/types/BlogPostT';
import { getFailureMessage } from '/src/api/utils/getFailureMessage';
import { authNav } from '/src/auth/routes';
import { SaveBlogPostResultT } from '/src/blogPosts/BlogPostsState';
import { blogPostsNav } from '/src/blogPosts/routes';
import { blogsNav } from '/src/blogs/routes';
import { getNameError } from '/src/forms/utils/getNameError';
import { navTo } from '/src/routes/navHandler';

const BLOG_POST_GONE_MESSAGE = 'This blog post no longer exists';

const getInitialValues = (blogPost: BlogPostT) => {
  return {
    'blogPostForm.title': blogPost.title ?? null,
    'blogPostForm.content': blogPost.content ?? null,
    'blogPostForm.level': blogPost.level ?? null,
    'blogPostForm.isTransient': blogPost.isTransient ?? null,
  };
};

const getInitialErrors = (props: PropsT & typeof ContextProps) => {
  return {};
};

const getHandleValidate =
  (props: PropsT & typeof ContextProps) =>
  ({ values, setError }: HandleValidateArgsT) => {
    const titleError = getNameError(values['blogPostForm.title']);
    if (titleError) {
      setError('blogPostForm.title', titleError);
    }
  };

// Returns the form field that a failed save belongs to, and its message.
const getSaveError = (
  error: CreateBlogPostErrorT | UpdateBlogPostErrorT
): [string, string] => {
  switch (error.code) {
    case 'BLOG_POST_TITLE_ALREADY_EXISTS':
      return ['blogPostForm.title', 'A blog post with this title already exists'];
    case 'FORM_CONTAINS_FORBIDDEN_WORDS':
      return [
        `blogPostForm.${error.fieldName}`,
        'This field contains forbidden words',
      ];
    case 'BLOG_POST_NOT_FOUND':
      return ['global', BLOG_POST_GONE_MESSAGE];
    case 'UNEXPECTED':
      return ['global', getFailureMessage(error.cause)];
  }
};

const getHandleSubmit =
  (
    props: PropsT & typeof ContextProps,
    initialValues: FormState['values'],
    initialErrors: FormState['errors']
  ) =>
  ({ formState, values }: HandleSubmitArgsT) => {
    // The list no longer has this blog post, so there's nothing left to save
    if (!props.blogPostsAddition.item && !props.blogPost) {
      formState.setError('global', BLOG_POST_GONE_MESSAGE);
      return Promise.resolve();
    }

    return props.blogPostsEdit
      .save({
        values: unflatten({
          ...values,
          'blogPostForm.title': values['blogPostForm.title'],
          'blogPostForm.content': values['blogPostForm.content'],
          'blogPostForm.level': values['blogPostForm.level'],
        }),
      })
      .then((result: SaveBlogPostResultT) => {
        if (!result.ok) {
          formState.setError(...getSaveError(result.error));
          return;
        }
        formState.reset(initialValues, initialErrors);
        navTo(
          blogPostsNav.blogPost({
            blogSlug: props.blog.slug,
            blogPostSlug: result.value.slug,
          })
        );
      });
  };

const getHandleCancel =
  (props: PropsT & typeof ContextProps) =>
  ({ formState }: HandleCancelArgsT) => {
    const mustRestore = !!props.blogPostsAddition.item;
    const isBlogPostGone = !mustRestore && !props.blogPost;
    props.blogPostsEdit.cancel();
    if (isBlogPostGone) {
      navTo(blogsNav.blog({ blogSlug: props.blog.slug }));
    }
    if (mustRestore) {
      if (!props.navState.restoreNavPoint()) {
        navTo(authNav.home({}));
      }
    }
  };

export const form = {
  getHandleValidate,
  getHandleSubmit,
  getHandleCancel,
  getInitialValues,
  getInitialErrors,
};
