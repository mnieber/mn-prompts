// The outcome of an action. A failed request is a result too: either a domain condition
// (e.g. a name that is already taken), or an UnexpectedErrorT (e.g. a network error). Only
// a bug in our code rejects the promise.
export type ResultT<ValueT, ErrorT> =
  | { ok: true; value: ValueT }
  | { ok: false; error: ErrorT };

export const ok = <ValueT = void>(value?: ValueT) => {
  return { ok: true as const, value: value as ValueT };
};

export const err = <ErrorT extends object>(error: ErrorT) => {
  return { ok: false as const, error };
};

export type UnexpectedErrorT = { code: 'UNEXPECTED'; cause: unknown };

export const unexpectedErr = (cause: unknown) => {
  return err({ code: 'UNEXPECTED' as const, cause });
};
