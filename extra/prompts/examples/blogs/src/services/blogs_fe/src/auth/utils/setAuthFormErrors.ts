import { FormState } from 'react-form-state-context';
import { AuthFormErrorT } from '/src/api/utils/allauth';
import { getFailureMessage } from '/src/api/utils/getFailureMessage';

// Shows the errors of a failed request. An error of a field that the form doesn't have
// (e.g. the key from the link in the email) is shown as a global error.
export const setAuthFormErrors = (
  formState: FormState,
  error: AuthFormErrorT,
  fieldNames: string[]
) => {
  switch (error.code) {
    case 'INVALID_FIELDS':
      Object.entries(error.fieldErrors).forEach(([name, message]) => {
        formState.setError(
          fieldNames.includes(name) ? name : 'global',
          message
        );
      });
      return;
    case 'UNEXPECTED':
      formState.setError('global', getFailureMessage(error.cause));
      return;
  }
};
