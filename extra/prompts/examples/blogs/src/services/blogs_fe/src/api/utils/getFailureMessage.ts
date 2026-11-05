// The message for a failure that has no specific message of its own.
export const getFailureMessage = (error: any) => {
  return error?.response?.status === 403
    ? "You don't have permission to do this"
    : 'Oops, something went wrong, please try again later';
};
