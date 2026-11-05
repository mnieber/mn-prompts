import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { authPost } from '/src/api/restClient';
import {
  AuthFormErrorT,
  authFormFailure,
  authUrl,
} from '/src/api/utils/allauth';
import { ok, ResultT } from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

export type ResetPasswordArgsT = {
  key: string;
  password: string;
};

export type ResetPasswordResultT = ResultT<void, AuthFormErrorT>;

export function resetPassword(
  args: ResetPasswordArgsT
): Promise<ResetPasswordResultT> {
  return authPost(`${authUrl}/password/reset`, args).then(
    () => waitOnDev(1000, ok()),
    (error) =>
      // The password has changed, and the user can now sign in
      waitOnDev(
        1000,
        error.response?.status === 401 ? ok() : authFormFailure(error)
      )
  );
}

export const useResetPassword = () => {
  return useObservableMutation({
    mutationFn: resetPassword,
  });
};
