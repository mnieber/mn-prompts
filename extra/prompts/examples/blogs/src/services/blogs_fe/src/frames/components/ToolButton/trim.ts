import { IconS } from '/src/frames/components/Icon';
import { cn } from '/src/utils/classnames';
import { ModeOverlayT } from '/src/utils/trim';

export const ToolButtonS = {
  color: {
    gray: () => cn('text-gray-text'),
    grayDisabled: () => cn('text-gray-300'),
  },
  Icon: {
    size: {
      medium: () => cn([IconS.size.s32(), 'p-2']),
      small: () => cn([IconS.size.s24(), 'p-1']),
    },
    margin: {
      medium: () => cn('mr-2'),
      none: () => cn(),
    },
    color: {
      grayFill: () => cn('fill-gray-text'),
      grayFillDisabled: () => cn('fill-gray-300'),
      grayBackground: () => cn('bg-gray-text'),
      grayBackgroundDisabled: () => cn('fill-gray-300 !bg-[#999999]'),
    },
  },
};

export type ToolButtonTrimT = {
  base: {
    componentName: string;
    root: {
      color: any;
    };
    Icon: {
      margin: any;
      size: any;
      color: any;
    };
  };
  disabled?: ModeOverlayT<ToolButtonTrimT>;
};

export const DefaultToolButtonTrim = {
  // These are applied to the root element and the Icon.
  base: {
    componentName: 'ToolButton',
    root: {
      color: ToolButtonS.color.gray(),
    },
    Icon: {
      size: ToolButtonS.Icon.size.medium(),
      margin: ToolButtonS.Icon.margin.medium(),
      color: ToolButtonS.Icon.color.grayBackground(),
    },
  },
  // These are layered on top if the ToolButton is disabled.
  disabled: {
    root: { color: ToolButtonS.color.grayDisabled() },
    Icon: { color: ToolButtonS.Icon.color.grayBackgroundDisabled() },
  },
};
