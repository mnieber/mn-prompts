import { ModeOverlayT } from '/src/utils/trim';

export type ActionButtonTrimT = {
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
  danger?: ModeOverlayT<ActionButtonTrimT>;
  disabled?: ModeOverlayT<ActionButtonTrimT>;
};

export const ActionButtonS = {
  color: {
    disabled: () => 'text-gray-400 hover:text-gray-400 border-gray-400',
    blueWithDarkText: () => 'bg-blue-400 text-blue-darkest hover:bg-blue-600',
    redWithWhiteText: () =>
      'text-red-400 hover:text-red-300 border-red-400 hover:border-red-300',
  },
  border: {
    none: () => '',
  },
  fontSize: {
    medium: () => 'text-base',
    big: () => 'text-lg',
  },
  padding: {
    medium: () => 'px-4 py-2',
    big: () => 'px-6 py-4',
  },
};

export const DefaultActionButtonTrim = {
  base: {
    componentName: 'Default',
    root: {
      color: ActionButtonS.color.blueWithDarkText(),
      border: ActionButtonS.border.none(),
      fontSize: ActionButtonS.fontSize.medium(),
      padding: ActionButtonS.padding.medium(),
    },
  },
  danger: {
    root: {
      color: ActionButtonS.color.redWithWhiteText(),
    },
  },
  disabled: {
    root: {
      color: ActionButtonS.color.disabled(),
    },
  },
};
