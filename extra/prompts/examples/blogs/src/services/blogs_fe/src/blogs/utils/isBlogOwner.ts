import { BlogT } from '/src/api/types/BlogT';
import { AuthState } from '/src/auth/AuthState';

export const isBlogOwner = (blog: BlogT | undefined, authState: AuthState) => {
  return !!blog && !!authState.accountId && blog.ownerId === authState.accountId;
};
