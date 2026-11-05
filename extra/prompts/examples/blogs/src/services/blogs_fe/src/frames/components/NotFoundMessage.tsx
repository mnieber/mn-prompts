import { observer } from 'mobx-react-lite';
import { DelayedFlag } from '/src/utils/DelayedFlag';
import { cn } from '/src/utils/classnames';
import { useBuilder } from '/src/utils/hooks';

export type PropsT = {
  isMissing: boolean;
  message: string;
  className?: any;
};

// The delay avoids a flash while a list is still being refetched
export const NotFoundMessage = observer((props: PropsT) => {
  const showMessage = useBuilder(() => new DelayedFlag());
  showMessage.update(props.isMissing);

  return showMessage.flag ? (
    <div className={cn('NotFoundMessage', 'my-4', props.className)}>
      {props.message}
    </div>
  ) : null;
});
