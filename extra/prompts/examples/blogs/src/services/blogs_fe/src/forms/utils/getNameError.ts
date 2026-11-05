const MAX_NAME_LENGTH = 200;

// The error for a value that is used as a name or a title.
export const getNameError = (value: string | null | undefined) => {
  const name = (value ?? '').trim();
  if (!name) {
    return 'This field is required';
  }
  return name.length > MAX_NAME_LENGTH ? 'This field is too long' : undefined;
};
