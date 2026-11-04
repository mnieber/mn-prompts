// A mutation resolves with { success: false } for the errors that it knows. For other
// errors, ObservableMutation.mutateAsync resolves with the error itself.
export const isFailedMutation = (response: any) => {
  return response instanceof Error || response?.success === false;
};
