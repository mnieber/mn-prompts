import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { queryClient } from '/src/api/queryClient';
import { authDelete } from '/src/api/restClient';
import { authUrl } from '/src/api/utils/allauth';
import { AuthState, anonymous } from '/src/auth/AuthState';
import { ObjT } from '/src/utils/types';

export type SignOutArgsT = {};

export function signOut(args: SignOutArgsT) {
  return authDelete(`${authUrl}/session`).catch((error) => {
    // After signing out, the session endpoint says that nobody is signed in
    if (error.response?.status === 401) {
      return { errors: [] };
    }
    throw error;
  });
}

export const useSignOut = (authState?: AuthState) => {
  const queryName = 'signOut';

  return useObservableMutation({
    mutationFn: signOut,
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      // We completely clear the query cache so that the anonymous user
      // will never see results from the previous user.
      queryClient.getQueryCache().clear();
      if (authState) authState.onUpdated(queryName, data);
      authState?.setUserId(anonymous);
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
