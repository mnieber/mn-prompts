import { cn } from '/src/utils/classnames';

export type PropsT = React.PropsWithChildren<{
  className?: any;
}>;

export const MainView = (props: PropsT) => {
  return (
    <div className={cn('MainView', props.className)}>{props.children}</div>
  );
};
