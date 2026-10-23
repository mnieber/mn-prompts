import { z } from 'zod';

export const convertDataToCamelCase = <T extends z.ZodTypeAny>(
  schema: T,
  data: any
): any => {
  if (schema instanceof z.ZodObject) {
    if (typeof data !== 'object' || data === null) {
      return data;
    }
    const newData: any = {};
    for (const [key, value] of Object.entries(schema.shape)) {
      const snakeCaseKey = key.replace(
        /[A-Z]/g,
        (letter) => `_${letter.toLowerCase()}`
      );
      if (snakeCaseKey in data) {
        newData[key] = convertDataToCamelCase(
          value as z.ZodTypeAny,
          data[snakeCaseKey]
        );
      }
    }
    return newData;
  }

  if (schema instanceof z.ZodArray) {
    if (!Array.isArray(data)) {
      return data;
    }
    return data.map((item) => convertDataToCamelCase(schema.element, item));
  }

  if (schema instanceof z.ZodOptional || schema instanceof z.ZodNullable) {
    return data === undefined || data === null
      ? data
      : convertDataToCamelCase(schema.unwrap(), data);
  }

  if (schema instanceof z.ZodLazy) {
    // Resolve the lazy schema and recurse
    return convertDataToCamelCase(schema.schema, data);
  }

  // For primitive types, no transformation needed
  return data;
};
