import { ObjT } from '/src/utils/types';

// Returns the detail of the first error with this code.
export const getErrorDetail = (responseData: ObjT, errorCode: string) => {
  return responseData['errors'].find((x: ObjT) => x.code === errorCode)?.detail;
};
