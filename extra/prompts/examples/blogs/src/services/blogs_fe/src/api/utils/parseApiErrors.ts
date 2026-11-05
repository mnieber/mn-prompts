import { z } from 'zod';

const ApiErrorsSchema = z.object({
  errors: z.array(
    z.object({
      code: z.string(),
      detail: z.string(),
    })
  ),
});

// Returns the errors in the body of a failed response. Not every response has them: the
// body is undefined after a network error, and it can come from something other than our
// api (e.g. the html of a 502).
export const parseApiErrors = (responseData: unknown) => {
  const parsed = ApiErrorsSchema.safeParse(responseData);
  return parsed.success ? parsed.data.errors : [];
};
