import { ObjT } from '/src/utils/types';

export const bindActionsCtr = (actionsCtr: ObjT, state: any) => {
  Object.keys(actionsCtr).forEach((key) => {
    actionsCtr[key] = actionsCtr[key].bind(state);
  });
};
