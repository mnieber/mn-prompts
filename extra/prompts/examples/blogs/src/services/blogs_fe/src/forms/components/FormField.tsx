import { observer } from 'mobx-react-lite';
import { IconS } from '/src/frames/components/Icon';
import { cn } from '/src/utils/classnames';

// Import styles
import './FormField.AuthCard.scss';
import './FormField.MainView.scss';

export type PropsT = React.PropsWithChildren<{
  componentClassName?: string;
  className?: any;
}>;

export const FormField = observer((props: PropsT) => {
  const name = props.componentClassName ?? 'FormField';

  return (
    <div className={cn(name, 'flex flex-col', props.className)}>
      {props.children}
    </div>
  );
});

export const FormFieldS = {
  Input: () => 'py-2 px-3 grow',
  Button: {
    root: () => 'FormField__Button',
    gap: () => 'mr-0.5',
  },
  Icon: () => cn('mr-2', IconS.size.s20()),
};
