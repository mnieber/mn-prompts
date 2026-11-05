import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { authPost } from '/src/api/restClient';
import {
  authUrl,
  hasPendingFlow,
  parseAllauthErrors,
  SessionSchema,
} from '/src/api/utils/allauth';
import {
  err,
  ok,
  ResultT,
  unexpectedErr,
  UnexpectedErrorT,
} from '/src/api/utils/result';
import { AuthState, Anonymous, anonymous } from '/src/auth/AuthState';
import { invalidateLoadUserId, loadUserId } from '/src/auth/endpoints/queries';
import { waitOnDev } from '/src/utils/wait';

export type SignInArgsT = {
  userId: string;
  password: string;
};

export type SignInResultT = ResultT<
  { userId: string; accountId: string },
  SignInErrorT
>;
export type SignInRefusedErrorT =
  | { code: 'INVALID_CREDENTIALS' }
  | { code: 'EMAIL_NOT_VERIFIED' }
  | { code: 'INACTIVE_ACCOUNT' }
  | { code: 'TOO_MANY_ATTEMPTS' };
export type SignInErrorT = SignInRefusedErrorT | UnexpectedErrorT;

const getSignInFailure = (
  error: any
): Promise<SignInResultT> | SignInResultT => {
  const data = error.response?.data;
  switch (error.response?.status) {
    case 400: {
      const isRateLimited = parseAllauthErrors(data).some(
        (x) => x.code === 'too_many_login_attempts'
      );
      return err({
        code: isRateLimited ? 'TOO_MANY_ATTEMPTS' : 'INVALID_CREDENTIALS',
      });
    }
    case 401:
      return err({
        code: hasPendingFlow(data, 'verify_email')
          ? 'EMAIL_NOT_VERIFIED'
          : 'INACTIVE_ACCOUNT',
      });
    case 409:
      // Already signed in (e.g. in another tab)
      return loadUserId().then(
        (x: { userId: string | Anonymous; accountId: string }) =>
          x.userId === anonymous
            ? unexpectedErr(error)
            : ok({ userId: x.userId as string, accountId: x.accountId })
      );
    default:
      return unexpectedErr(error);
  }
};

export function signIn(args: SignInArgsT): Promise<SignInResultT> {
  return authPost(`${authUrl}/login`, {
    email: args.userId,
    password: args.password,
  }).then(
    (response) => {
      const parsed = SessionSchema.safeParse(response.data);
      return waitOnDev(
        1000,
        parsed.success
          ? ok({
              userId: parsed.data.data.user.email,
              accountId: parsed.data.data.user.id,
            })
          : unexpectedErr(parsed.error)
      );
    },
    (error) =>
      Promise.resolve(getSignInFailure(error)).then((x) => waitOnDev(1000, x))
  );
}

export const useSignIn = (authState?: AuthState) => {
  const queryName = 'signIn';

  return useObservableMutation({
    mutationFn: signIn,
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (result) => {
      if (result.ok) {
        authState?.onUpdated(queryName, {});
        authState?.setUserId(result.value.userId, result.value.accountId);
        invalidateLoadUserId({});
        return;
      }
      authState?.setUserId(anonymous);
      if (result.error.code === 'UNEXPECTED') {
        authState?.onErrored(queryName, String(result.error.cause));
        return;
      }
      authState?.onUpdated(queryName, {
        errors: [result.error.code],
      });
      invalidateLoadUserId({});
    },
  });
};
