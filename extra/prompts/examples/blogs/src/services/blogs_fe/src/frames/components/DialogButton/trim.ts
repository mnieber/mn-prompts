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
    blueWithDarkText: () => 'bg-blue-400 text-blue-darkest hover:bg-blue-600',
    tealWithDarkText: () => 'bg-teal-400 text-teal-darkest hover:bg-teal-600',
    tealWithWhiteText: () => 'bg-teal-400 text-white hover:bg-teal-300',
    skyBlueWithWhiteText: () => 'bg-blue-400 text-white hover:bg-blue-300',
    withSkyBlueText: () => 'text-blue-400 hover:text-blue-600',
    withWhiteText: () => 'text-gray-900 hover:text-white',
    withTealText: () => 'text-teal-400 hover:text-teal-600',
    skyBlueWithDarkText: () =>
      'bg-blue-400 text-blue-darkest hover:bg-blue-600',
    redWithWhiteText: () => 'bg-red-400 text-white hover:bg-red-600',
    grayBackground: () => 'bg-gray-500 hover:bg-gray-500',
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
