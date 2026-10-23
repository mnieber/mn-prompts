import { createBrowserHistory } from 'history';
import { createObservableHistory } from 'mobx-observable-history';
import { flags } from '/src/app/flags';

export const history = patchHistory(createBrowserHistory());
export const navigation = createObservableHistory(history);

export function patchHistory(history: any) {
  var push = history.push;
  history.push = function (state: any) {
    if (typeof history.onpush == 'function') {
      history.onpush({ state: state });
    }
    if (flags.logHistory) {
      console.log('history.push', arguments[0]);
    }
    return push.apply(history, arguments);
  };

  var replace = history.replace;
  history.replace = function (state: any) {
    if (typeof history.onreplace == 'function') {
      history.onreplace({ state: state });
    }
    if (flags.logHistory) {
      console.log('history.replace', arguments[0]);
    }
    return replace.apply(history, arguments);
  };
  return history;
}
