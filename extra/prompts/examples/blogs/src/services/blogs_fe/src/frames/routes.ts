import { history } from '/src/routes/history';
import { navHandler, RouteSpecT } from '/src/routes/navHandler';
import { generatePath } from '/src/routes/utils/generatePath';

export const framesRoutes = {
  dashboard: () => '/blogs',
};

export class FramesNav {
  dashboard(params: {}, callerId?: string): RouteSpecT {
    return navHandler().run('dashboard', params, callerId);
  }
}

export class DefaultFramesNavHandler extends FramesNav {
  dashboard(params: {}, callerId?: string) {
    return {
      url: generatePath(framesRoutes.dashboard(), {}),
      nav: history.push,
    };
  }
}

export const framesNav = new FramesNav();
