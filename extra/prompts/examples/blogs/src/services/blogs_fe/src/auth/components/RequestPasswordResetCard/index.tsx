import { observer } from 'mobx-react-lite';
import React from 'react';
import { useMessages } from './useMessages';
import { AuthCard, AuthCardS } from '/src/auth/components/AuthCard';
import { RequestPasswordResetForm } from '/src/auth/components/RequestPasswordResetForm';
import { useRequestPasswordReset } from '/src/auth/endpoints';
import { authNav } from '/src/auth/routes';
import { L } from '/src/frames/layout';
import { RouterLink } from '/src/routes/components';
import { cn } from '/src/utils/classnames';

export const RequestPasswordResetCard = observer(() => {
  const { messages } = useMessages();
  const run = useRequestPasswordReset().run;
  const [isDone, setIsDone] = React.useState(false);

  return (
    //
    // 🔳 RequestPasswordResetCard 🔳
    //
    <AuthCard id="RequestPasswordResetCard">
      {isDone ? (
        <div className={cn('RequestPasswordResetCard__Done', [L.col.banner()])}>
          {messages.divDone}
        </div>
      ) : (
        <RequestPasswordResetForm
          className={cn(AuthCardS.Form())}
          submit={(values: any) =>
            run({ email: values.email }).then((result) => {
              setIsDone(result.ok);
              return result;
            })
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
