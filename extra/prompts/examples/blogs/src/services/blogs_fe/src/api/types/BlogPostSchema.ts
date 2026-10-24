import { z } from 'zod';
import { BlogPostT } from '/src/api/types/BlogPostT';
import { EntitySchema } from '/src/api/types/EntitySchema';

export const BlogPostLevelSchema = z.union([
  z.literal('easy'),
  z.literal('medium'),
  z.literal('hard'),
]);

export const BlogPostSchema: z.ZodType<BlogPostT> = z.object({
  ...EntitySchema.shape,
  title: z.string(),
  content: z.string(),
  slug: z.string(),
  isPublished: z.boolean(),
  level: BlogPostLevelSchema,
  // tags: z.array(z.string()),
  isTransient: z.boolean().optional(),
});
