import { createBrowserHistory } from 'history';
import { createObservableHistory } from 'mobx-observable-history';
import { flags } from '/src/app/flags';

export const history = patchHistory(createBrowserHistory());
export const navigation = createObservableHistory(history);

export function patchHistory(history: any) {
  const push = history.push;
  history.push = function (...args: any[]) {
    const state = args[0];
    if (typeof history.onpush == 'function') {
      history.onpush({ state: state });
    }
    if (flags.logHistory) {
      console.log('history.push', state);
    }
    return push.apply(history, args);
  };

  const replace = history.replace;
  history.replace = function (...args: any[]) {
    const state = args[0];
    if (typeof history.onreplace == 'function') {
      history.onreplace({ state: state });
    }
    if (flags.logHistory) {
      console.log('history.replace', state);
    }
    return replace.apply(history, args);
  };
  return history;
}
