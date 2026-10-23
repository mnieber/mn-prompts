import { action, makeObservable, observable } from 'mobx';

export class DelayedFlag {
  @observable flag: boolean = false;
  timeout?: NodeJS.Timeout;
  delay: number = 1000;

  @action setFlag(flag: boolean) {
    this.flag = flag;
  }

  @action update(flag: boolean) {
    if (!flag) {
      this.setFlag(false);
      if (this.timeout) {
        clearTimeout(this.timeout);
        this.timeout = undefined;
      }
    } else {
      if (!this.flag && !this.timeout) {
        this.timeout = setTimeout(() => {
          this.setFlag(true);
          this.timeout = undefined;
        }, 1000);
      }
    }
  }

  constructor(delay: number = 1000) {
    this.delay = delay;
    makeObservable(this);
  }
}
