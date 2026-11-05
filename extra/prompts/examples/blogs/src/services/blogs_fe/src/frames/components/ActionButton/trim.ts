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
  };
  danger?: ModeOverlayT<ActionButtonTrimT>;
  disabled?: ModeOverlayT<ActionButtonTrimT>;
};

export const ActionButtonS = {
  color: {
    disabled: () => 'cursor-not-allowed border-line bg-canvas text-ink-faint',
    neutral: () => 'border-line bg-surface text-ink hover:bg-canvas',
    accent: () =>
      'border-accent bg-accent text-white hover:border-accent-hover hover:bg-accent-hover',
    danger: () =>
      'border-line bg-surface text-danger hover:border-danger hover:bg-danger-soft',
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
};

export const DefaultActionButtonTrim = {
  base: {
    componentName: 'Default',
    root: {
      color: ActionButtonS.color.neutral(),
      border: ActionButtonS.border.none(),
      fontSize: ActionButtonS.fontSize.small(),
      padding: ActionButtonS.padding.small(),
    },
  },
  danger: {
    root: {
      color: ActionButtonS.color.danger(),
    },
  },
  disabled: {
    root: {
      color: ActionButtonS.color.disabled(),
    },
  },
};
