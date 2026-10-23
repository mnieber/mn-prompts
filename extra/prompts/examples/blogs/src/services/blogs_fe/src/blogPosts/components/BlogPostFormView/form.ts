import * as R from 'ramda';
import {
  FormState,
  HandleCancelArgsT,
  HandleSubmitArgsT,
  HandleValidateArgsT,
  unflatten,
} from 'react-form-state-context';
import { ContextProps, PropsT } from './index';
import { authNav } from '/src/auth/routes';
import { blogPostsNav } from '/src/blogPosts/routes';
import { navTo } from '/src/routes/navHandler';
import { ObjT } from '/src/utils/types';

const getInitialValues = (props: PropsT & typeof ContextProps) => {
  const blogPost = props.blogPostsAddition.item ?? props.blogPost;

  return {
    'blogPostForm.title': blogPost.title ?? null,
    'blogPostForm.slug': blogPost.slug ?? null,
    'blogPostForm.content': blogPost.content ?? null,
    'blogPostForm.level': blogPost.level ?? null,
    'blogPostForm.tags': blogPost.tags ?? null,
    'blogPostForm.isTransient': blogPost.isTransient ?? null,
  };
};

const getInitialErrors = (props: PropsT & typeof ContextProps) => {
  return {};
};

const getHandleValidate =
  (props: PropsT & typeof ContextProps) =>
  ({ values, setError }: HandleValidateArgsT) => {
    if (R.isNil(values['blogPostForm.title'])) {
      setError('blogPostForm.title', 'This field is required');
    }
  };

const getHandleSubmit =
  (
    props: PropsT & typeof ContextProps,
    initialValues: FormState['values'],
    initialErrors: FormState['errors']
  ) =>
  ({ formState, values }: HandleSubmitArgsT) => {
    return props.blogPostsEdit
      .save({
        values: unflatten({
          ...values,
          'blogPostForm.title': values['blogPostForm.title'],
          'blogPostForm.slug': values['blogPostForm.slug'],
          'blogPostForm.content': values['blogPostForm.content'],
          'blogPostForm.level': values['blogPostForm.level'],
          'blogPostForm.tags': values['blogPostForm.tags'],
        }),
      })
      .then((response: ObjT) => {
        formState.reset(initialValues, initialErrors);
        navTo(
          blogPostsNav.blogPost({
            blogSlug: props.blog.slug,
            blogPostSlug: response.data.slug,
          })
        );
        return response;
      })
      .catch((error: any) => {
        formState.setError(
          'global',
          'Oops, something went wrong, please try again later'
        );
      });
  };

const getHandleCancel =
  (props: PropsT & typeof ContextProps) =>
  ({ formState }: HandleCancelArgsT) => {
    const mustRestore = !!props.blogPostsAddition.item;
    props.blogPostsEdit.cancel();
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
