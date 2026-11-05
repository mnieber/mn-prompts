import {
  FormState,
  HandleCancelArgsT,
  HandleSubmitArgsT,
  HandleValidateArgsT,
  unflatten,
} from 'react-form-state-context';
import { ContextProps, PropsT } from './index';
import {
  CreateBlogErrorT,
  CreateBlogResultT,
} from '/src/api/mutations/useCreateBlog';
import { getFailureMessage } from '/src/api/utils/getFailureMessage';
import { authNav } from '/src/auth/routes';
import { blogsNav } from '/src/blogs/routes';
import { getNameError } from '/src/forms/utils/getNameError';
import { navTo } from '/src/routes/navHandler';

const getInitialValues = (props: PropsT & typeof ContextProps) => {
  const blog = props.blogsAddition.item || props.blog;
  return {
    'blogForm.name': blog.name ?? null,
    'blogForm.description': blog.description ?? null,
    'blogForm.isTransient': blog.isTransient ?? null,
  };
};

const getInitialErrors = (props: PropsT & typeof ContextProps) => {
  return {};
};

const getHandleValidate =
  (props: PropsT & typeof ContextProps) =>
  ({ values, setError }: HandleValidateArgsT) => {
    const nameError = getNameError(values['blogForm.name']);
    if (nameError) {
      setError('blogForm.name', nameError);
    }
  };

// Returns the form field that a failed save belongs to, and its message.
const getSaveError = (error: CreateBlogErrorT): [string, string] => {
  switch (error.code) {
    case 'BLOG_NAME_ALREADY_EXISTS':
      return ['blogForm.name', 'A blog with this name already exists'];
    case 'FORM_CONTAINS_FORBIDDEN_WORDS':
      return [
        `blogForm.${error.fieldName}`,
        'This field contains forbidden words',
      ];
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
    return props.blogsEdit
      .save({
        values: unflatten({
          ...values,
          'blogForm.name': values['blogForm.name'],
          'blogForm.description': values['blogForm.description'],
        }),
      })
      .then((result: CreateBlogResultT) => {
        if (!result.ok) {
          formState.setError(...getSaveError(result.error));
          return;
        }
        formState.reset(initialValues, initialErrors);
        navTo(blogsNav.blog({ blogSlug: result.value.slug }));
      });
  };

const getHandleCancel =
  (props: PropsT & typeof ContextProps) =>
  ({ formState }: HandleCancelArgsT) => {
    const mustRestore = !!props.blogsAddition.item;
    props.blogsEdit.cancel();
    if (mustRestore) {
      navTo(props.navState.navPoint ?? authNav.home({}));
    }
  };

export const form = {
  getHandleValidate,
  getHandleSubmit,
  getHandleCancel,
  getInitialValues,
  getInitialErrors,
};
