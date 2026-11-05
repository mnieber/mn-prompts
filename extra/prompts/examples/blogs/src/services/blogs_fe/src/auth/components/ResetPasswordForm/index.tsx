import { FormStateProvider } from 'react-form-state-context';
import { form } from './form';
import { useMessages } from './useMessages';
import { AuthFormErrorT } from '/src/api/utils/allauth';
import { ResultT } from '/src/api/utils/result';
import { AuthFormS } from '/src/auth/components/AuthForm';
import {
  Field,
  FormSaveButton,
  GlobalError,
  PasswordField,
} from '/src/forms/components';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

export const formFields = {
  password: 'password',
  passwordConfirmation: 'passwordConfirmation',
};

export type PropsT = {
  submit: (values: any) => Promise<ResultT<void, AuthFormErrorT>>;
  className?: any;
};

export function ResetPasswordForm(props: PropsT) {
  const { messages } = useMessages();

  return (
    //
    // 🔳 FormStateProvider 🔳
    //
    <FormStateProvider
      initialValues={form.getInitialValues()}
      initialErrors={{}}
      handleValidate={form.getHandleValidate(messages)}
      handleSubmit={form.getHandleSubmit(props)}
    >
      {
        // 🔳 ResetPasswordForm 🔳
      }
      <div
        className={cn('ResetPasswordForm', [L.col.banner(), props.className])}
      >
        <GlobalError className={AuthFormS.GlobalError()} />

        {
          // 🔳 password 🔳
        }
        <Field
          className={AuthFormS.Field()}
          fieldName={formFields.password}
          tabOnEnter={true}
        >
          <PasswordField placeholder="New password" />
        </Field>

        {
          // 🔳 passwordConfirmation 🔳
        }
        <Field
          className={AuthFormS.Field()}
          fieldName={formFields.passwordConfirmation}
          submitOnEnter={true}
        >
          <PasswordField placeholder="Confirm new password" />
        </Field>

        {
          // 🔳 FormSaveButton 🔳
        }
        <FormSaveButton
          theme="AuthCard"
          label={messages.labelChangePassword}
          className={cn(AuthFormS.Button())}
        />
      </div>
    </FormStateProvider>
  );
}
