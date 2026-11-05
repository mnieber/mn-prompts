import { observer } from 'mobx-react-lite';
import React from 'react';
import { useMessages } from './useMessages';
import { AuthCard, AuthCardS } from '/src/auth/components/AuthCard';
import { ResetPasswordForm } from '/src/auth/components/ResetPasswordForm';
import { useResetPassword } from '/src/auth/endpoints';
import { authNav } from '/src/auth/routes';
import { L } from '/src/frames/layout';
import { RouterLink } from '/src/routes/components';
import { cn } from '/src/utils/classnames';
import { useSearchAndUrlParams } from '/src/utils/hooks/useSearchAndUrlParams';

export const ResetPasswordCard = observer(() => {
  const { messages } = useMessages();
  const run = useResetPassword().run;
  const [isDone, setIsDone] = React.useState(false);
  const params = useSearchAndUrlParams();

  return (
    //
    // 🔳 ResetPasswordCard 🔳
    //
    <AuthCard id="ResetPasswordCard">
      {isDone ? (
        <div className={cn('ResetPasswordCard__Done', [L.col.banner()])}>
          {messages.divDone}
        </div>
      ) : (
        <ResetPasswordForm
          className={cn(AuthCardS.Form())}
          submit={(values: any) =>
            run({
              key: decodeURIComponent(params.key),
              password: values.password,
            }).then((result) => {
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
