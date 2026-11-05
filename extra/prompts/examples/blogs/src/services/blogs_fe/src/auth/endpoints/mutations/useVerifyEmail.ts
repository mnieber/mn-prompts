import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { authPost } from '/src/api/restClient';
import {
  AuthFormErrorT,
  authFormFailure,
  authUrl,
} from '/src/api/utils/allauth';
import { ok, ResultT } from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

export type VerifyEmailArgsT = {
  key: string;
};

export type VerifyEmailResultT = ResultT<void, AuthFormErrorT>;

export function verifyEmail(
  args: VerifyEmailArgsT
): Promise<VerifyEmailResultT> {
  return authPost(`${authUrl}/email/verify`, args).then(
    () => waitOnDev(1000, ok()),
    (error) =>
      // The email address is verified, and the user can now sign in
      waitOnDev(
        1000,
        error.response?.status === 401 ? ok() : authFormFailure(error)
      )
  );
}

export const useVerifyEmail = () => {
  return useObservableMutation({
    mutationFn: verifyEmail,
  });
};
