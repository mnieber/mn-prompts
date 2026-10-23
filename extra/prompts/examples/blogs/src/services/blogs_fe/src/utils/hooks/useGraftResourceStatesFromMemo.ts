import { runInAction } from 'mobx';
import {
  GraftResourceStatesArgsT,
  graftResourceStates,
  shareRS,
} from 'mobx-resource-states';
import React from 'react';

export type ArgsT = {
  saveMemory?: boolean; // default to true
};

export const useGraftResourceStatesFromMemo = (args: ArgsT) => {
  const prevResourcesRef = React.useRef<any[] | null>(null);
  const saveMemory = args.saveMemory ?? true;

  return (args: Omit<GraftResourceStatesArgsT, 'prevResources'>): any[] => {
    runInAction(() => {
      graftResourceStates({
        ...args,
        resources: args.resources ?? [],
        prevResources: prevResourcesRef.current ?? [],
      });
    });

    // If saveMemory, then instead of keeping a reference to args.resources, we create
    // a look-up table for the resource states.
    const keyProp = args.keyProp ?? 'id';
    prevResourcesRef.current = saveMemory
      ? (args.resources ?? []).reduce((acc, resource) => {
          const obj = { [keyProp]: resource[keyProp] };
          shareRS(resource, obj);
          acc.push(obj);
          return acc;
        }, [])
      : args.resources;
    return args.resources;
  };
};
