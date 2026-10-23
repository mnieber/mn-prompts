import { ObjT } from '/src/utils/types';

export const hasErrorCode = (responseData: ObjT, errorCodes: string[]) => {
  for (const error of responseData['errors']) {
    if (errorCodes.includes(error.code)) {
      return true;
    }
  }
  return false;
};
