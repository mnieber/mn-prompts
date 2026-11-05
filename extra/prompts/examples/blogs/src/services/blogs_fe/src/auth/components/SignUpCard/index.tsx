import { observer } from 'mobx-react-lite';
import React from 'react';
import { useMessages } from './useMessages';
import { AuthCard, AuthCardS } from '/src/auth/components/AuthCard';
import { SignUpForm } from '/src/auth/components/SignUpForm';
import { useSignUp } from '/src/auth/endpoints';
import { authNav } from '/src/auth/routes';
import { L } from '/src/frames/layout';
import { RouterLink } from '/src/routes/components';
import { cn } from '/src/utils/classnames';

export const SignUpCard = observer(() => {
  const { messages } = useMessages();
  const run = useSignUp().run;
  const [isDone, setIsDone] = React.useState(false);

  return (
    //
    // 🔳 SignUpCard 🔳
    //
    <AuthCard id="SignUpCard">
      {isDone ? (
        <div className={cn('SignUpCard__Done', [L.col.banner()])}>
          {messages.divDone}
        </div>
      ) : (
        <SignUpForm
          className={cn(AuthCardS.Form())}
          submit={(values: any) =>
            run({ email: values.email, password: values.password }).then(
              (result) => {
                setIsDone(result.ok);
                return result;
              }
            )
          }
        />
      )}

      {
        // 🔳 Sign in link 🔳
      }
      <div className={cn(AuthCardS.CardFooter(), [L.col.banner()])}>
        <RouterLink to={authNav.signIn({}).url}>
          {messages.labelBackToSignIn}
        </RouterLink>
      </div>
    </AuthCard>
  );
});
