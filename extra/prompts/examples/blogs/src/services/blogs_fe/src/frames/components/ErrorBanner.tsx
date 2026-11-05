import { observer } from 'mobx-react-lite';
import { errorBannerState } from '/src/frames/errorBannerState';
import { cn } from '/src/utils/classnames';

// Import styles
import './ErrorBanner.scss';

export type PropsT = {
  className?: any;
};

export const ErrorBanner = observer((props: PropsT) => {
  if (!errorBannerState.message) {
    return null;
  }

  return (
    <div className={cn('ErrorBanner', props.className)} role="alert">
      <span>{errorBannerState.message}</span>
      <button type="button" onClick={() => errorBannerState.clear()}>
        Dismiss
      </button>
    </div>
  );
});
