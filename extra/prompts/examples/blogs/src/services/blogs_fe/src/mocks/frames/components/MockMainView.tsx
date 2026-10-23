import { cn } from '/src/utils/classnames';

export type PropsT = React.PropsWithChildren<{
  className?: any;
}>;

export const MockMainView = (props: PropsT) => {
  return (
    <div className={cn('MockMainView', props.className)}>{props.children}</div>
  );
};
