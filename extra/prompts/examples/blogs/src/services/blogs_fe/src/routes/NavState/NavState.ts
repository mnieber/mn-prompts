import { action, makeObservable, observable } from 'mobx';
import * as R from 'ramda';
import { history } from '/src/routes/history';
import { RouteSpecT, navTo } from '/src/routes/navHandler';
import { pathname } from '/src/utils/urls';

export class NavState {
  @observable navPoint?: RouteSpecT;

  @action storeNavPoint() {
    this.navPoint = {
      url: pathname(),
      nav: history.push,
    };
  }

  @action restoreNavPoint() {
    if (R.isNil(this.navPoint)) return false;
    navTo(this.navPoint!);
    return true;
  }

  get hasNavPoint() {
    return !R.isNil(this.navPoint);
  }

  constructor() {
    makeObservable(this);
  }
}
