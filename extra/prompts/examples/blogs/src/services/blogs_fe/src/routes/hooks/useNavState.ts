import { NavState } from '/src/routes/NavState';
import { useBuilder } from '/src/utils/hooks/useBuilder';

export type PropsT = {};

export const useNavState = (props: PropsT) => {
  const navState = useBuilder(() => {
    return new NavState();
  });

  return {
    navState,
  };
};
