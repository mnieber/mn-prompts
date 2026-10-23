import { useFormStateContext } from 'react-form-state-context';
import { cn } from '/src/utils/classnames';

// Import styles
import './GlobalError.scss';

type PropsT = {
  className?: any;
  error?: any;
};

export const GlobalError = (props: PropsT) => {
  const formState = useFormStateContext();
  const globalError = props.error ?? formState.errors['global'];

  return globalError ? (
    <div className={cn('GlobalError', props.className)}>{globalError}</div>
  ) : null;
};
