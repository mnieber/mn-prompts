import { FormStateProvider } from 'react-form-state-context';
import { form } from './form';
import { useMessages } from './useMessages';
import { AuthFormErrorT } from '/src/api/utils/allauth';
import { ResultT } from '/src/api/utils/result';
import { AuthFormS } from '/src/auth/components/AuthForm';
import {
  EmailField,
  Field,
  FormSaveButton,
  GlobalError,
  PasswordField,
} from '/src/forms/components';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

export const formFields = {
  email: 'email',
  password: 'password',
  passwordConfirmation: 'passwordConfirmation',
};

export type PropsT = {
  submit: (values: any) => Promise<ResultT<void, AuthFormErrorT>>;
  className?: any;
};

export function SignUpForm(props: PropsT) {
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
        // 🔳 SignUpForm 🔳
      }
      <div className={cn('SignUpForm', [L.col.banner(), props.className])}>
        <GlobalError className={AuthFormS.GlobalError()} />

        {
          // 🔳 email 🔳
        }
        <Field
          className={AuthFormS.Field()}
          fieldName={formFields.email}
          tabOnEnter={true}
        >
          <EmailField autoFocus={true} placeholder="Email" />
        </Field>

        {
          // 🔳 password 🔳
        }
        <Field
          className={AuthFormS.Field()}
          fieldName={formFields.password}
          tabOnEnter={true}
        >
          <PasswordField placeholder="Password" />
        </Field>

        {
          // 🔳 passwordConfirmation 🔳
        }
        <Field
          className={AuthFormS.Field()}
          fieldName={formFields.passwordConfirmation}
          submitOnEnter={true}
        >
          <PasswordField placeholder="Confirm password" />
        </Field>

        {
          // 🔳 FormSaveButton 🔳
        }
        <FormSaveButton
          theme="AuthCard"
          label={messages.labelSignUp}
          className={cn(AuthFormS.Button())}
        />
      </div>
    </FormStateProvider>
  );
}
