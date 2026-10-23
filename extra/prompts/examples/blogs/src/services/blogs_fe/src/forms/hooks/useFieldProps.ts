import React from 'react';
import {
  createFormFieldProps,
  FormState,
  useFormStateContext,
} from 'react-form-state-context';
import {
  FormFieldContextPropsT,
  useFormFieldContext,
} from '/src/forms/components';
import { tabToNext } from '/src/forms/utils';

type FieldTypeT = 'checkbox' | 'text' | 'password';

export type FieldPropsT = {
  controlled?: boolean;
  disabled?: boolean;
  fieldType: FieldTypeT;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onFocus?: (e: React.FocusEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  autoFocus?: boolean;
  autoSelect?: boolean;
  tabIndex?: number;
  inputRef?: any;
};

export const useFieldProps = (props: FieldPropsT) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  const { fieldName } = fieldContext;

  const formFieldProps = React.useMemo(
    () =>
      createFormFieldProps({
        formState,
        fieldName: fieldName,
        fieldType: props.fieldType,
        onChange: props.onChange,
        controlled: props.controlled,
      }),
    [formState, fieldName, props.fieldType, props.onChange, props.controlled]
  );

  const {
    onFocus,
    onKeyDown,
    autoSelect,
    inputRef,
    fieldType,
    controlled,
    onChange,
    ...rest
  } = props;

  return {
    ...formFieldProps,
    onFocus: (e: React.FocusEvent<HTMLInputElement>) => {
      onFocus && onFocus(e);
      if (autoSelect) {
        setTimeout(() => {
          e.target.select();
        }, 0);
      }
    },
    ref: inputRef,
    onKeyDown: handleKeyDown(fieldContext, formState, onKeyDown),
    controlled: controlled ? 'true' : undefined,
    ...rest,
  };
};

export function handleKeyDown(
  fieldContext: FormFieldContextPropsT,
  formState: FormState,
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void
) {
  return (e: any) => {
    if (e.keyCode === 13) {
      if (fieldContext.submitOnEnter) {
        formState.submit();
      } else if (fieldContext.tabOnEnter ?? true) {
        e.preventDefault();
        tabToNext(e);
      }
    } else {
      if (onKeyDown) {
        onKeyDown(e);
      }
    }
  };
}
