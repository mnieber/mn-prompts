import { FormState } from 'react-form-state-context';
import { formFields as ff, PropsT } from './index';
import { setAuthFormErrors } from '/src/auth/utils/setAuthFormErrors';
import { ObjT } from '/src/utils/types';

const getInitialValues = () => {
  return {
    [ff.email]: null,
  };
};

const getHandleValidate =
  (messages: ObjT) =>
  ({
    values,
    setError,
  }: {
    values: FormState['values'];
    setError: FormState['setError'];
  }) => {
    if (!values[ff.email]) {
      setError(ff.email, messages.divPleaseEnterYourEmailAddress);
    }
  };

const getHandleSubmit =
  (props: PropsT) =>
  ({
    formState,
    values,
  }: {
    formState: FormState;
    values: FormState['values'];
  }) => {
    return props.submit(values).then((result) => {
      if (!result.ok) {
        setAuthFormErrors(formState, result.error, [ff.email]);
      }
    });
  };

export const form = {
  getInitialValues,
  getHandleValidate,
  getHandleSubmit,
};
