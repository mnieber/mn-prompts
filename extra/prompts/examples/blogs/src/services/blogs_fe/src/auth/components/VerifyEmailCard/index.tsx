import { observer } from 'mobx-react-lite';
import React from 'react';
import { FormState, FormStateProvider } from 'react-form-state-context';
import { useMessages } from './useMessages';
import { AuthCard, AuthCardS } from '/src/auth/components/AuthCard';
import { AuthFormS } from '/src/auth/components/AuthForm';
import { useVerifyEmail } from '/src/auth/endpoints';
import { authNav } from '/src/auth/routes';
import { setAuthFormErrors } from '/src/auth/utils/setAuthFormErrors';
import { FormSaveButton, GlobalError } from '/src/forms/components';
import { L } from '/src/frames/layout';
import { RouterLink } from '/src/routes/components';
import { cn } from '/src/utils/classnames';
import { useSearchAndUrlParams } from '/src/utils/hooks/useSearchAndUrlParams';

// The user presses a button to verify. This way, an email scanner that opens the link
// doesn't verify the address.
export const VerifyEmailCard = observer(() => {
  const { messages } = useMessages();
  const verifyEmail = useVerifyEmail().run;
  const params = useSearchAndUrlParams();
  const [isDone, setIsDone] = React.useState(false);

  return (
    //
    // 🔳 VerifyEmailCard 🔳
    //
    <AuthCard id="VerifyEmailCard">
      {isDone ? (
        <div className={cn('VerifyEmailCard__Done', [L.col.banner()])}>
          {messages.divDone}
        </div>
      ) : (
        <FormStateProvider
          initialValues={{}}
          initialErrors={{}}
          handleValidate={() => {}}
          handleSubmit={({ formState }: { formState: FormState }) => {
            return verifyEmail({ key: decodeURIComponent(params.key) }).then(
              (result) => {
                if (result.ok) {
                  setIsDone(true);
                } else {
                  setAuthFormErrors(formState, result.error, []);
                }
              }
            );
          }}
        >
          <div
            className={cn('VerifyEmailForm', [
              L.col.banner(),
              AuthCardS.Form(),
            ])}
          >
            <GlobalError className={AuthFormS.GlobalError()} />
            <FormSaveButton
              theme="AuthCard"
              label={messages.labelVerifyEmail}
              className={cn(AuthFormS.Button())}
            />
          </div>
        </FormStateProvider>
      )}

      {
        // 🔳 Sign in link 🔳
      }
      <div className={cn(AuthCardS.CardFooter(), [L.col.banner()])}>
        <RouterLink to={authNav.signIn({}).url}>
          {messages.labelGoToSignIn}
        </RouterLink>
      </div>
    </AuthCard>
  );
});
