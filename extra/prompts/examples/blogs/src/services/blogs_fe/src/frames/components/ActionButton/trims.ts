import {
  ActionButtonS,
  type ActionButtonTrimT,
  DefaultActionButtonTrim,
} from '/src/frames/components/ActionButton';
import { createTrim } from '/src/utils/trim';

export const AccentActionButtonTrim: ActionButtonTrimT = createTrim(
  DefaultActionButtonTrim,
  {
    base: {
      componentName: 'Accent-ActionButton',
      root: {
        color: ActionButtonS.color.accent(),
      },
    },
  }
);
