import { authNav } from '/src/auth/routes';
import { RouterLink } from '/src/routes/components';

export const useMessages = () => {
  const divChangedYourMind = (
    <div>
      Changed your mind? You can return to the{' '}
      <RouterLink to={authNav.home({}).url}>home</RouterLink> page.
    </div>
  );

  return {
    messages: {
      divChangedYourMind,
      createAccount: 'Create An Account',
    },
  };
};
