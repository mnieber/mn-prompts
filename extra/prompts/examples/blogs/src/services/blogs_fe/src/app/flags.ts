import { observable } from 'mobx';

export const flags = observable({
  logQueries: true,
  logSkandha: true,
  logResourceStates: true,
  logHistory: false,
  logStateProviders: false,
  useMsw: false,
  mockApp: false,
  // Use the playground that runs with yarn fake (see tests/playgrounds)
  useFakeBackend: false,
});
