import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { authPost } from '/src/api/restClient';
import {
  AuthFormErrorT,
  authFormFailure,
  authUrl,
} from '/src/api/utils/allauth';
import { ok, ResultT } from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

export type SignUpArgsT = {
  email: string;
  password: string;
};

export type SignUpResultT = ResultT<void, AuthFormErrorT>;

export function signUp(args: SignUpArgsT): Promise<SignUpResultT> {
  return authPost(`${authUrl}/signup`, args).then(
    () => waitOnDev(1000, ok()),
    (error) =>
      // The account exists now, and verifying the email address is the pending step
      waitOnDev(
        1000,
        error.response?.status === 401 ? ok() : authFormFailure(error)
      )
  );
}

export const useSignUp = () => {
  return useObservableMutation({
    mutationFn: signUp,
  });
};
