import { z } from 'zod';
import { EntityT } from '/src/api/types/EntityT';
import { assertTypesEqual } from '/src/utils/types';

export const EntitySchema = z.object({
  id: z.string(),
});

assertTypesEqual<EntityT, z.infer<typeof EntitySchema>>(true);
