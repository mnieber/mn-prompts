import { z } from 'zod';
import { convertDataToCamelCase } from '/src/api/utils/convertDataToCamelCase';
import { ObjT } from '/src/utils/types';
import { AnyZodSchema } from '/src/utils/zod';

export const parseResponse = <SchemaT extends AnyZodSchema>(
  schema: SchemaT,
  data: ObjT
): z.infer<SchemaT> => {
  try {
    const transformedData = convertDataToCamelCase(schema, data);
    return schema.parse(transformedData);
  } catch (error) {
    console.error(error);
    return data;
  }
};
