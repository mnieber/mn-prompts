import { observer } from 'mobx-react-lite';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { navTo, RouteSpecT } from '/src/routes/navHandler';

type PropsT = {
  getRoute: Function;
};

const ContextProps = {};

export const RedirectEffect = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const route = props.getRoute() as RouteSpecT;
    React.useEffect(() => {
      if (route) {
        navTo(route);
      }
    }, [route]);

    return null;
  }, ContextProps)
);
