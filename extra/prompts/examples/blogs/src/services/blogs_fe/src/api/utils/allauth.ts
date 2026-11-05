import { z } from 'zod';
import { err, unexpectedErr, UnexpectedErrorT } from '/src/api/utils/result';

// The endpoints of allauth, relative to the host url
export const authUrl = '/_allauth/browser/v1/auth';

// The response of allauth when a user is signed in
export const SessionSchema = z.object({
  data: z.object({
    user: z.object({
      id: z.string(),
      email: z.string(),
    }),
  }),
});

const ErrorsSchema = z.object({
  errors: z.array(
    z.object({
      code: z.string(),
      message: z.string(),
      param: z.string().optional(),
    })
  ),
});

const FlowsSchema = z.object({
  data: z.object({
    flows: z.array(
      z.object({
        id: z.string(),
        is_pending: z.boolean().optional(),
      })
    ),
  }),
});

// Returns the errors in the body of a failed response. These have a different format
// than the errors of our own api (see parseApiErrors).
export const parseAllauthErrors = (responseData: unknown) => {
  const parsed = ErrorsSchema.safeParse(responseData);
  return parsed.success ? parsed.data.errors : [];
};

// Whether a 401 response says that the user must still complete this step.
export const hasPendingFlow = (responseData: unknown, flowId: string) => {
  const parsed = FlowsSchema.safeParse(responseData);
  return (
    parsed.success &&
    parsed.data.data.flows.some((x) => x.id === flowId && x.is_pending)
  );
};

export type InvalidFieldsErrorT = {
  code: 'INVALID_FIELDS';
  // The message of each field. An error without a field is stored under `global`.
  fieldErrors: Record<string, string>;
};
export type AuthFormErrorT = InvalidFieldsErrorT | UnexpectedErrorT;

// Returns the result for a failed request of an auth form.
export const authFormFailure = (error: any) => {
  const errors = parseAllauthErrors(error.response?.data);
  if (errors.length === 0) {
    return unexpectedErr(error);
  }
  const fieldErrors: Record<string, string> = {};
  errors.forEach((x) => {
    fieldErrors[x.param ?? 'global'] ??= x.message;
  });
  return err({ code: 'INVALID_FIELDS' as const, fieldErrors });
};
