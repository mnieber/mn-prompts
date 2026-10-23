export type ObjT = { [key: string]: any };

export const isString = (x: any) => {
  return typeof x === 'string' || x instanceof String;
};

export type RecursivePartial<T> = {
  [P in keyof T]?: T[P] extends (infer U)[]
    ? RecursivePartial<U>[]
    : T[P] extends object | undefined
    ? RecursivePartial<T[P]>
    : T[P];
};

export type Exactly<T, U> = T extends U
  ? U extends T
    ? unknown
    : never
  : never;

export const assertTypesEqual = <T, U>(_: Exactly<T, U>) => {};
