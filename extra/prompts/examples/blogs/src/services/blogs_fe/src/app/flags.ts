import { observable } from 'mobx';

export const flags = observable({
  logQueries: true,
  logSkandha: true,
  logResourceStates: true,
  logHistory: false,
  logStateProviders: false,
  useMsw: false,
  mockApp: false,
});
