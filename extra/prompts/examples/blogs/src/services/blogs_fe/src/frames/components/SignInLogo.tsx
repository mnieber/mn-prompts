import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './SignInLogo.scss';

export type PropsT = {};

export const SignInLogo = (props: PropsT) => {
  return (
    //
    // 🔳🔳 SignInLogo__SubTitle
    //
    <div className={cn('SignInLogo', L.col.skewer())}>
      <div className={cn('SignInLogo__Title', [L.row.banner()])}>
        <div className={cn('SignInLogo__TitlePrefix')}>Blog</div>
        <div className={cn('SignInLogo__TitleSuffix')}>Manager</div>
      </div>
    </div>
  );
};
