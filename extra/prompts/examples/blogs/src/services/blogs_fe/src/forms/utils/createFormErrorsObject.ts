import * as R from 'ramda';
import { ObjT } from '/src/utils/types';

export const createFormErrorsObject = (): ObjT => {
  const formErrors: ObjT = {};
  // This line ensures that the formErrors object can be decoded. The formErrors object
  // may have circular references, therefore, we only keep the keys.
  formErrors.toJSON = () => JSON.stringify(R.keys(formErrors));
  return formErrors;
};

export const getErrorKeys = (formErrors: ObjT) => {
  return R.keys(formErrors).filter((x) => x !== 'toJSON');
};
