import { observer } from 'mobx-react-lite';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { useNavState } from '/src/routes/hooks/useNavState';
import { NavStateContext } from '/src/routes/hooks/useNavStateContext';
import { createGetProps } from '/src/utils/createGetProps';

export type PropsT = React.PropsWithChildren<{}>;

const ContextProps = {};

export const NavStateProvider = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const { navState } = useNavState({});

    const getNavStateContext = () => {
      return createGetProps({
        navState: () => navState,
      });
    };

    return (
      <NavStateContext.Provider value={getNavStateContext()}>
        {props.children}
      </NavStateContext.Provider>
    );
  }, ContextProps)
);
