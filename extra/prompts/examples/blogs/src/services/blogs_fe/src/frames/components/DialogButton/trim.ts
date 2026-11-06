import { IconS } from '/src/frames/components/Icon';
import { ModeOverlayT } from '/src/utils/trim';

export type DialogButtonTrimT = {
  base: {
    componentName: string;
    root: {
      border: any;
      color: any;
      fontSize: any;
      padding: any;
    };
    Icon: {
      margin: any;
      size: any;
      color: any;
    };
  };
  danger?: ModeOverlayT<DialogButtonTrimT>;
  disabled?: ModeOverlayT<DialogButtonTrimT>;
};

export const DialogButtonS = {
  color: {
    disabled: () => 'cursor-not-allowed bg-canvas text-ink-faint',
    accent: () => 'bg-accent text-white hover:bg-accent-hover',
    quiet: () => 'text-ink-soft hover:bg-canvas hover:text-ink',
    danger: () => 'bg-danger text-white hover:bg-danger-hover',
  },
  border: {
    none: () => '',
  },
  fontSize: {
    small: () => 'text-sm',
    medium: () => 'text-base',
    big: () => 'text-lg',
  },
  padding: {
    small: () => 'px-4 py-1.5',
    medium: () => 'px-4 py-2',
    big: () => 'px-6 py-4',
  },
  Icon: {
    margin: {
      medium: () => 'mr-2',
    },
  },
};

export const DefaultDialogButtonTrim = {
  base: {
    componentName: 'Default',
    root: {
      color: DialogButtonS.color.accent(),
      border: DialogButtonS.border.none(),
      fontSize: DialogButtonS.fontSize.small(),
      padding: DialogButtonS.padding.small(),
    },
    Icon: {
      margin: DialogButtonS.Icon.margin.medium(),
      size: IconS.size.s20(),
      color: IconS.color.gray(),
    },
  },
  danger: undefined,
  disabled: {
    root: {
      color: DialogButtonS.color.disabled(),
    },
  },
};
