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
import { blogsNav } from '/src/blogs/routes';
import { navTo } from '/src/routes/navHandler';
import { ObjT } from '/src/utils/types';

const getInitialValues = (props: PropsT & typeof ContextProps) => {
  const blog = props.blogsAddition.item || props.blog;
  return {
    'blogForm.name': blog.name ?? null,
    'blogForm.slug': blog.slug ?? null,
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
    if (R.isNil(values['blogForm.name'])) {
      setError('blogForm.name', 'This field is required');
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
          'blogForm.slug': values['blogForm.slug'],
          'blogForm.description': values['blogForm.description'],
        }),
      })
      .then((response: ObjT) => {
        formState.reset(initialValues, initialErrors);
        navTo(blogsNav.blog({ blogSlug: response.data.slug }));
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
