import { observer } from 'mobx-react-lite';
import { DelayedFlag } from '/src/utils/DelayedFlag';
import { cn } from '/src/utils/classnames';
import { useBuilder } from '/src/utils/hooks';

export type PropsT = {
  resourceName: string;
  isInSync: boolean;
  className?: any;
};

export const UrlEffectView = observer((props: PropsT) => {
  const raiseError = useBuilder(() => new DelayedFlag());
  raiseError.update(!props.isInSync);

  if (raiseError.flag) {
    const msg = `${props.resourceName} is not in sync with the url`;
    console.error(msg);
    return import.meta.env.DEV ? (
      <div className={cn('text-2xl bg-white text-red', props.className)}>
        {msg}
      </div>
    ) : null;
  }

  return null;
});
