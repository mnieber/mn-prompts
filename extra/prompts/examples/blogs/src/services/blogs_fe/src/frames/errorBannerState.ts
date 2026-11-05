import { action, makeObservable, observable } from 'mobx';

// The error that the ErrorBanner shows, for failures that happen outside of a form.
class ErrorBannerState {
  @observable message: string | undefined = undefined;

  constructor() {
    makeObservable(this);
  }

  @action show(message: string) {
    this.message = message;
  }

  @action clear() {
    this.message = undefined;
  }
}

export const errorBannerState = new ErrorBannerState();
