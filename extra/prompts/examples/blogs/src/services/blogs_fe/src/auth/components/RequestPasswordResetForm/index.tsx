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
} from '/src/forms/components';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

export const formFields = {
  email: 'email',
};

export type PropsT = {
  submit: (values: any) => Promise<ResultT<void, AuthFormErrorT>>;
  className?: any;
};

export function RequestPasswordResetForm(props: PropsT) {
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
        // 🔳 RequestPasswordResetForm 🔳
      }
      <div
        className={cn('RequestPasswordResetForm', [
          L.col.banner(),
          props.className,
        ])}
      >
        <GlobalError className={AuthFormS.GlobalError()} />

        {
          // 🔳 email 🔳
        }
        <Field
          className={AuthFormS.Field()}
          fieldName={formFields.email}
          submitOnEnter={true}
        >
          <EmailField autoFocus={true} placeholder="Email" />
        </Field>

        {
          // 🔳 FormSaveButton 🔳
        }
        <FormSaveButton
          theme="AuthCard"
          label={messages.labelSendResetLink}
          className={cn(AuthFormS.Button())}
        />
      </div>
    </FormStateProvider>
  );
}
