import { observer } from 'mobx-react-lite';
import { AuthPage, AuthPageS } from '/src/auth/components/AuthPage';
import { SignInCard } from '/src/auth/components/SignInCard';
import { SignInLogo } from '/src/frames/components/SignInLogo';
import { cn } from '/src/utils/classnames';

export const SignInPage = observer(() => {
  return (
    <AuthPage className="flex-grow">
      <SignInLogo />
      <div className={cn(AuthPageS.Gap())} />
      <SignInCard />
    </AuthPage>
  );
});
