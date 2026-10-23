import {
  DefaultDialogButtonTrim,
  DialogButtonS,
  type DialogButtonTrimT,
} from '/src/frames/components/DialogButton';
import { IconS } from '/src/frames/components/Icon';
import { createTrim } from '/src/utils/trim';

export const BlueDialogButtonTrim: DialogButtonTrimT = createTrim(
  DefaultDialogButtonTrim,
  {
    base: {
      componentName: 'Blue-DialogButton',
      root: {
        color: DialogButtonS.color.blueWithDarkText(),
      },
      Icon: {
        color: IconS.color.blueDarkest(),
      },
    },
    disabled: {
      root: {
        color: DialogButtonS.color.disabled(),
      },
    },
  }
);

export const TealDialogButtonTrim: DialogButtonTrimT = createTrim(
  DefaultDialogButtonTrim,
  {
    base: {
      componentName: 'Teal-DialogButton',
      root: {
        color: DialogButtonS.color.tealWithDarkText(),
      },
      Icon: {
        color: DialogButtonS.color.tealWithDarkText(),
      },
    },
  }
);

export const TealWithWhiteTextDialogButtonTrim: DialogButtonTrimT = createTrim(
  DefaultDialogButtonTrim,
  {
    base: {
      componentName: 'TealWithWhiteText-DialogButton',
      root: {
        color: DialogButtonS.color.tealWithWhiteText(),
      },
      Icon: {
        color: DialogButtonS.color.tealWithWhiteText(),
      },
    },
  }
);

export const SkyBlueWithBorderDialogButtonTrim: DialogButtonTrimT = createTrim(
  DefaultDialogButtonTrim,
  {
    base: {
      componentName: 'SkyBlueWithBorder-DialogButton',
      root: {
        border: 'border-2 border-blue-primary',
        color: DialogButtonS.color.withSkyBlueText(),
      },
      Icon: {
        color: IconS.color.bluePrimary(),
      },
    },
  }
);
