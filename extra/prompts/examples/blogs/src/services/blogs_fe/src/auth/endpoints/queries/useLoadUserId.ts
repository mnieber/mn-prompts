import { useQuery } from '@tanstack/react-query';
import { queryClient } from '/src/api/queryClient';
import { authGet } from '/src/api/restClient';
import { authUrl, SessionSchema } from '/src/api/utils/allauth';
import { createQueryKey } from '/src/api/utils/createQueryKey';
import { AuthState, anonymous } from '/src/auth/AuthState';

// Loading the session also sets the CSRF cookie, which the next writes need.
export function loadUserId(): Promise<any> {
  return authGet(`${authUrl}/session`)
    .then((response) => {
      const { user } = SessionSchema.parse(response.data).data;
      return { userId: user.email, accountId: user.id };
    })
    .catch(() => {
      // A 401 means that nobody is signed in
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
      return loadUserId().then((data) => {
        if (authState) authState.setUserId(data.userId, data.accountId);
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
