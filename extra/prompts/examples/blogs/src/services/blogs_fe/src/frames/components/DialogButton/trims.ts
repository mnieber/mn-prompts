import {
  DefaultDialogButtonTrim,
  DialogButtonS,
  type DialogButtonTrimT,
} from '/src/frames/components/DialogButton';
import { createTrim } from '/src/utils/trim';

export const QuietDialogButtonTrim: DialogButtonTrimT = createTrim(
  DefaultDialogButtonTrim,
  {
    base: {
      componentName: 'Quiet-DialogButton',
      root: {
        color: DialogButtonS.color.quiet(),
      },
    },
  }
);
