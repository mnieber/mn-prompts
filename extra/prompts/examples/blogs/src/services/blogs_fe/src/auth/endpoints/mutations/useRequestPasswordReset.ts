import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { authPost } from '/src/api/restClient';
import {
  AuthFormErrorT,
  authFormFailure,
  authUrl,
} from '/src/api/utils/allauth';
import { ok, ResultT } from '/src/api/utils/result';
import { waitOnDev } from '/src/utils/wait';

export type RequestPasswordResetArgsT = {
  email: string;
};

export type RequestPasswordResetResultT = ResultT<void, AuthFormErrorT>;

export function requestPasswordReset(
  args: RequestPasswordResetArgsT
): Promise<RequestPasswordResetResultT> {
  return authPost(`${authUrl}/password/request`, args).then(
    () => waitOnDev(1000, ok()),
    (error) => waitOnDev(1000, authFormFailure(error))
  );
}

export const useRequestPasswordReset = () => {
  return useObservableMutation({
    mutationFn: requestPasswordReset,
  });
};
