import { action, makeObservable, observable } from 'mobx';
import { useBuilder } from '/src/utils/hooks';
import { ObjT } from '/src/utils/types';

export type MutationStatusT = 'idle' | 'loading' | 'success' | 'error';

export type ArgsT<MutationArgsT = any> = {
  mutationFn: (args: MutationArgsT) => Promise<any> | void;
  onMutate?: (args: MutationArgsT) => Promise<any> | void;
  onSuccess?: (response: ObjT, args: MutationArgsT) => Promise<any> | void;
  onError?: (error: Error, args: MutationArgsT) => void;
};

export class ObservableMutation<MutationArgsT = any> {
  status = 'idle';
  mutationFn: (args: MutationArgsT) => Promise<any> | void;
  onMutate?: (args: MutationArgsT) => Promise<any> | void;
  onSuccess?: (response: ObjT, args: MutationArgsT) => Promise<any> | void;
  onError?: (error: Error, args: MutationArgsT) => void;

  setStatus = (status: MutationStatusT) => {
    this.status = status;
  };

  mutateAsync = (args: MutationArgsT) => {
    this.setStatus('loading');
    return Promise.resolve(this.onMutate ? this.onMutate(args) : undefined)
      .then(() => this.mutationFn(args))
      .then((response: any) => {
        return Promise.resolve(
          this.onSuccess ? this.onSuccess(response, args) : undefined
        ).then(() => {
          this.setStatus('success');
          return response;
        });
      })
      .catch((error: any) => {
        return Promise.resolve(
          this.onError ? this.onError(error, args) : undefined
        ).then(() => {
          this.setStatus('error');
          return error;
        });
      });
  };

  constructor(args: ArgsT<MutationArgsT>) {
    this.mutationFn = args.mutationFn;
    this.onSuccess = args.onSuccess;
    this.onError = args.onError;
    this.onMutate = args.onMutate;

    makeObservable(this, {
      status: observable,
      setStatus: action,
    });
  }
}

export const isRunning = (observableMutation: ObservableMutation) => {
  return observableMutation.status === 'loading';
};

export const useObservableMutation = <MutationArgsT = any>(
  args: ArgsT<MutationArgsT>
) => {
  return useBuilder(() => new ObservableMutation<MutationArgsT>(args));
};
