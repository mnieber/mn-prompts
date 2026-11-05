import { parseApiErrors } from '/src/api/utils/parseApiErrors';
import { err, unexpectedErr } from '/src/api/utils/result';

type KnownFailureT<FieldsT> = {
  [CodeT in keyof FieldsT]: {
    ok: false;
    error: { code: CodeT } & FieldsT[CodeT];
  };
}[keyof FieldsT];

// Returns the result for a failed request. The handlers map each known error code to the
// extra fields of its error. The first error in the response that has a handler decides
// the result. Without such an error, the result is an unexpected error.
export const requestFailure = <FieldsT extends Record<string, object>>(
  error: any,
  handlers: { [CodeT in keyof FieldsT]: (detail: string) => FieldsT[CodeT] }
): KnownFailureT<FieldsT> | ReturnType<typeof unexpectedErr> => {
  for (const { code, detail } of parseApiErrors(error.response?.data)) {
    if (Object.hasOwn(handlers, code)) {
      return err({ code, ...handlers[code](detail) }) as any;
    }
  }
  return unexpectedErr(error);
};

// The handler for an error code that has no extra fields.
export const noFields = () => ({});
