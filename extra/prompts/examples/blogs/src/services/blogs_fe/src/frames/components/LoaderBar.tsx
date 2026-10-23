import { observer } from 'mobx-react-lite';
import { withContextProps } from 'react-props-from-context';
import { cn } from '/src/utils/classnames';

// Import styles
import './LoaderBar.scss';

export type PropsT = {
  className?: any;
};

export const ContextProps = {};

export const LoaderBar = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    return <div className={cn('LoaderBar', props.className)}></div>;
  }, ContextProps)
);
