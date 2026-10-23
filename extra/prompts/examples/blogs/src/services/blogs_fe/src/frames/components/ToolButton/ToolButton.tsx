import { ButtonPropsT } from '/src/frames/components/ButtonPropsT';
import { Icon } from '/src/frames/components/Icon';
import {
  DefaultToolButtonTrim,
  ToolButtonTrimT,
} from '/src/frames/components/ToolButton/trim';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';
import { getMode, getModeCn } from '/src/utils/trim';

// Import styles
import './Modest-ToolButton.scss';
import './ToolButton.scss';

export type PropsT = {
  className?: any;
  trim?: ToolButtonTrimT;
  disabled?: boolean;
  iconName: string;
  label: string;
} & ButtonPropsT;

export const ToolButton = (props: PropsT) => {
  const trim = props.trim ?? DefaultToolButtonTrim;
  const mode = getMode(trim, { disabled: props.disabled });

  return (
    <button
      className={cn(
        trim.base.componentName,
        getModeCn(mode.root),
        { 'ToolButton--disabled': props.disabled },
        [L.row.skewer(), props.className]
      )}
      disabled={props.disabled}
      onClick={props.onClick}
    >
      <Icon className={getModeCn(mode.Icon)} name={props.iconName} />
      {props.label}
    </button>
  );
};
