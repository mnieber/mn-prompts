import { createNavHandler } from '/src/routes/createNavHandler';

export type RouteSpecT = {
  url: string;
  nav: (url: string) => void;
};

export class NavHandler {
  navHandlers: any[] = [];
  defaultNavHandlers: any[] = [];

  installNavHandler(navHandler: any) {
    this.navHandlers.push(navHandler);
  }

  installDefaultNavHandler(navHandler: any) {
    this.defaultNavHandlers.push(navHandler);
  }

  run(name: string, params: any, callerId?: string) {
    for (const handlers of [this.navHandlers, this.defaultNavHandlers]) {
      for (const navHandler of handlers) {
        const handlerFn = navHandler[name];
        if (!handlerFn) {
          continue;
        }

        const result = handlerFn(params, callerId);
        if (result) {
          return result;
        }
      }
    }
    throw new Error(`No nav handler found for ${name}`);
  }
}

export const navTo = (routeAndNav: RouteSpecT) => {
  routeAndNav.nav(routeAndNav.url);
};

export const ext = (route: string) => {
  return `${route}/*?`;
};

let _navHandler: NavHandler | undefined = undefined;

export const navHandler = () => {
  if (!_navHandler) {
    _navHandler = createNavHandler();
  }
  return _navHandler;
};
