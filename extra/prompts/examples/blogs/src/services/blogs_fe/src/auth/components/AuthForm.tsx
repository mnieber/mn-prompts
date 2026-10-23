// An AuthForm has:
// - a GlobalError. This component shows an error message with some space below it.
//   Note: if there is no global error, then no error - or space - is shown.
// - a Header. This is a text above the form, e.g. 'Enter your email and password to sign in'.
// - one or more Fields. A field is a wrapper around the form-field label, the form-field
//   and the form-field-error.
// - a Button, e.g. 'Sign In'.
export const AuthFormS = {
  GlobalError: () => 'mb-2',
  Header: () => 'mb-2',
  Field: () => 'mb-2',
  Button: () => '',
};
