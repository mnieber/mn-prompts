import { initRS } from 'mobx-resource-states';
import { EntityT } from '/src/api/types/EntityT';
import { createUUID } from '/src/utils/ids';
import { ObjT } from '/src/utils/types';

export type BlogT = EntityT & {
  name: string;
  description: string;
  slug: string;
  isTransient?: boolean;
};

export type BlogByIdT = { [id: string]: BlogT };

export const createBlog = (values: ObjT): BlogT => {
  return initRS({
    id: createUUID(),
    name: values.name ?? 'New blog',
    description: values.description ?? '',
    slug: values.slug ?? '-',
    isTransient: true,
  } as BlogT);
};
