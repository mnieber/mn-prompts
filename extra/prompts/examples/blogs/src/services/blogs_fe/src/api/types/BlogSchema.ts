import { z } from 'zod';
import { BlogT } from '/src/api/types/BlogT';
import { EntitySchema } from '/src/api/types/EntitySchema';

export const BlogSchema: z.ZodType<BlogT> = z.object({
  ...EntitySchema.shape,
  name: z.string(),
  description: z.string(),
  slug: z.string(),
  isTransient: z.boolean().optional(),
});
