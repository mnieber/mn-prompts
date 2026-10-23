import { useQuery } from '@tanstack/react-query';
import { queryClient } from '/src/api/queryClient';
import { get, getRefreshToken, setAuthTokens } from '/src/api/restClient';
import { createQueryKey } from '/src/api/utils/createQueryKey';
import { AuthState, anonymous } from '/src/auth/AuthState';
import { refreshToken } from '/src/auth/endpoints/mutations/refreshToken';
import { hasErrorCode } from '/src/auth/utils/hasErrorCode';
import { ObjT } from '/src/utils/types';

export type LoadUserIdArgsT = {
  maybeRefreshToken: boolean;
};

export function loadUserId(args: LoadUserIdArgsT): Promise<any> {
  const url = '/users/user-id/';

  return get(url)
    .then((response: ObjT) => {
      return {
        userId: response.data.user_id ?? anonymous,
      };
    })
    .catch((error: ObjT) => {
      if (
        hasErrorCode(error.response.data, ['authentication_failed']) &&
        getRefreshToken() &&
        args.maybeRefreshToken
      ) {
        // Try to refresh the token. Regardless of whether that worked, retry the
        // loadUserId, but this time with maybeRefreshToken set to false.
        return refreshToken().finally(() =>
          loadUserId({ maybeRefreshToken: false })
        );
      }

      // If we get here, then there was an unresolvable problem with the auth tokens,
      // and we've already tried to refresh them. In that case, clear the tokens and
      // throw an error.
      setAuthTokens(undefined, undefined);
      throw new Error(error.response);
    })
    .catch(() => {
      return {
        userId: anonymous,
      };
    });
}

export type QueryKeyT = {};

export function loadUserIdQueryKey(args: QueryKeyT) {
  return createQueryKey<QueryKeyT>('loadUserId', args);
}

export const useLoadUserId = (authState?: AuthState) => {
  return useQuery({
    queryKey: loadUserIdQueryKey({}),
    queryFn: () => {
      return loadUserId({ maybeRefreshToken: true }).then((data) => {
        if (authState) authState.setUserId(data.userId);
        return data;
      });
    },
  });
};

export const invalidateLoadUserId = (args: QueryKeyT) => {
  return queryClient.invalidateQueries({
    queryKey: loadUserIdQueryKey(args),
  });
};
