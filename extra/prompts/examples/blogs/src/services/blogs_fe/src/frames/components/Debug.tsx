import { cn } from '/src/utils/classnames';

// Import styles
import './SignInLogo.scss';

export type PropsT = {};

export const Debug = (props: PropsT) => {
  return (
    <div className={cn('Debug', 'text-white')}>
      <h1 className="text-3xl">Debug</h1>
    </div>
  );
};
