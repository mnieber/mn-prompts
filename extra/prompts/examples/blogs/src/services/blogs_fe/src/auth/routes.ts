import { history } from '/src/routes/history';
import { navHandler, RouteSpecT } from '/src/routes/navHandler';
import { generatePath } from '/src/routes/utils/generatePath';

export const authRoutes = {
  home: () => '/',
  signIn: () => '/sign-in',
  signUp: () => '/sign-up',
  verifyEmail: () => '/account/verify-email/:key',
  requestPasswordReset: () => '/account/password/reset',
  resetPassword: () => '/account/password/reset/:key',
};

export class AuthNav {
  home(params: {}, callerId?: string): RouteSpecT {
    return navHandler().run('home', params, callerId);
  }
  signIn(params: { nextUrl?: string }, callerId?: string): RouteSpecT {
    return navHandler().run('signIn', params, callerId);
  }
  signUp(params: {}, callerId?: string): RouteSpecT {
    return navHandler().run('signUp', params, callerId);
  }
  requestPasswordReset(params: {}, callerId?: string): RouteSpecT {
    return navHandler().run('requestPasswordReset', params, callerId);
  }
}

export class DefaultAuthNavHandler extends AuthNav {
  home(params: {}, callerId?: string) {
    return {
      url: generatePath(authRoutes.home(), {}),
      nav: history.push,
    };
  }
  signIn(params: { nextUrl?: string }, callerId?: string) {
    const suffix = params.nextUrl
      ? '?nextUrl=' + encodeURIComponent(params.nextUrl)
      : '';
    return {
      url: generatePath(authRoutes.signIn(), {}) + suffix,
      nav: history.push,
    };
  }
  signUp(params: {}, callerId?: string) {
    return {
      url: generatePath(authRoutes.signUp(), {}),
      nav: history.push,
    };
  }
  requestPasswordReset(params: {}, callerId?: string) {
    return {
      url: generatePath(authRoutes.requestPasswordReset(), {}),
      nav: history.push,
    };
  }
}

export const authNav = new AuthNav();
