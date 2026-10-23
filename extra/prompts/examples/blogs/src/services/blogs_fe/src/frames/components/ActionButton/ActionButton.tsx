import {
  ActionButtonTrimT,
  DefaultActionButtonTrim,
} from '/src/frames/components/ActionButton/trim';
import { ButtonPropsT } from '/src/frames/components/ButtonPropsT';
import { cn } from '/src/utils/classnames';
import { getMode, getModeCn } from '/src/utils/trim';

// Import styles
import './ActionButton.scss';

export type PropsT = {
  trim?: ActionButtonTrimT;
  danger?: boolean;
  disabled?: boolean;
  label: string;
  className?: any;
} & ButtonPropsT;

export type ActionButtonPropsT = PropsT;

export const ActionButton = (props: PropsT) => {
  const {
    className,
    danger: propsDanger,
    trim: propsTrim,
    disabled,
    label,
    ...rest
  } = props;

  const danger = propsDanger && !disabled;
  const trim = propsTrim ?? DefaultActionButtonTrim;
  const mode = getMode(trim, {
    danger,
    disabled,
  });

  return (
    /*
    🔳 ActionButton 🔳
    */
    <button
      disabled={disabled}
      className={cn(
        //
        trim.base.componentName,
        'ActionButton',
        [
          getModeCn(mode.root),
          'select-none',
          {
            'DialogButton--disabled': disabled,
            'DialogButton--danger': danger,
          },
        ],
        className
      )}
      {...rest}
    >
      {label}
    </button>
  );
};
