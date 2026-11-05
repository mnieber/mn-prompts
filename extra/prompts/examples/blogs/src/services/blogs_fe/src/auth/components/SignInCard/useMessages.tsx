import { authNav } from '/src/auth/routes';
import { RouterLink } from '/src/routes/components';

export const useMessages = () => {
  const divChangedYourMind = (
    <div>
      Changed your mind? You can return to the{' '}
      <RouterLink to={authNav.home({}).url}>home</RouterLink> page.
    </div>
  );

  const divForgotYourPassword = (
    <div>
      <RouterLink to={authNav.requestPasswordReset({}).url}>
        Did you forget your password?
      </RouterLink>
    </div>
  );

  const divCreateAccount = (
    <div>
      <RouterLink to={authNav.signUp({}).url}>Create an account</RouterLink>
    </div>
  );

  return {
    messages: {
      divChangedYourMind,
      divForgotYourPassword,
      divCreateAccount,
    },
  };
};
