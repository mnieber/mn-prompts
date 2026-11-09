import { runInAction } from 'mobx';
import React from 'react';
import { ObservableQuery, QueryDataT } from '/src/api/lib/ObservableQuery';
import { flags } from '/src/app/flags';
import { useBuilder } from '/src/utils/hooks/useBuilder';

export interface TanstackQuery {
  data: QueryDataT;
  isFetching: boolean;
  isInitialLoading: boolean;
}

export type OptionsT = {
  fetchAsLoad?: boolean;
  debugLabel?: string;
};

export const useObservableQuery = (
  query: TanstackQuery,
  options?: OptionsT
) => {
  const fetchAsLoad = options?.fetchAsLoad;
  const debugLabel = options?.debugLabel;

  const observableQuery = useBuilder(() => {
    const observableQuery = new ObservableQuery();
    observableQuery.debugLabel = debugLabel;
    updateObservableQuery(observableQuery, query, fetchAsLoad);
    return observableQuery;
  });

  // The tanstack query is a new object on each render, so the effect depends on its
  // fields (else it would update the observable query, and thereby cause a new render,
  // after each render)
  const { data, isFetching, isInitialLoading } = query;
  React.useEffect(() => {
    runInAction(() => {
      updateObservableQuery(
        observableQuery,
        { data, isFetching, isInitialLoading },
        fetchAsLoad
      );
      if (debugLabel && flags.logQueries) {
        observableQuery.log(
          `ObservableQuery ${observableQuery.id} (${debugLabel}) ` +
            `updated to ${observableQuery.status}`
        );
      }
    });
  }, [
    data,
    isFetching,
    isInitialLoading,
    observableQuery,
    fetchAsLoad,
    debugLabel,
  ]);

  return observableQuery;
};

const updateObservableQuery = (
  observableQuery: ObservableQuery,
  tanstackQuery: TanstackQuery,
  fetchAsLoad: boolean | undefined
) => {
  observableQuery.data = tanstackQuery.data;
  observableQuery.status =
    (fetchAsLoad && tanstackQuery.isFetching) || tanstackQuery.isInitialLoading
      ? 'loading'
      : 'idle';
};
