import { useFormStateContext } from 'react-form-state-context';
import {
  DefaultDialogButtonTrim,
  DialogButton,
  DialogButtonPropsT,
  DialogButtonS,
} from '/src/frames/components/DialogButton';
import { createTrim } from '/src/utils/trim';

export type PropsT = DialogButtonPropsT & { theme: 'MainView' };

export const FormCancelButton = (props: PropsT) => {
  const formState = useFormStateContext();
  const disabled = props.disabled || formState.getFlag('submitting');

  return (
    <DialogButton
      trim={
        props.theme === 'MainView'
          ? MainViewDialogButtonTrim
          : MainViewDialogButtonTrim
      }
      onClick={(e: any) => {
        e.preventDefault();
        formState.cancel();
      }}
      disabled={disabled}
      {...props}
    />
  );
};

const MainViewDialogButtonTrim = createTrim(DefaultDialogButtonTrim, {
  base: {
    componentName: 'FormCancelButton-DialogButton',
    root: {
      color: DialogButtonS.color.withSkyBlueText(),
    },
  },
  disabled: {
    root: {
      color: DialogButtonS.color.disabled(),
    },
  },
  danger: {
    root: {
      color: DialogButtonS.color.withWhiteText(),
    },
  },
});
