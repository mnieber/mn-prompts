import { observer } from 'mobx-react-lite';
import { useFormStateContext } from 'react-form-state-context';
import { useFormFieldContext } from '/src/forms/components';
import { tabToNext } from '/src/forms/utils';
import { cn } from '/src/utils/classnames';
import {
  PickerValueT,
  ValuePicker,
  PropsT as ValuePickerPropsT,
} from '/src/utils/components/ValuePicker';
import { useScheduledCall } from '/src/utils/hooks';
import { ObjT } from '/src/utils/types';

type PropsT<ValueT> = Omit<
  ValuePickerPropsT<ValueT> & {
    submitOnChange?: boolean;
  },
  'pickableValue'
>;

export const ValuePickerField = observer(<ValueT,>(props: PropsT<ValueT>) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();
  const formValue = formState.values[fieldContext.fieldName];
  const scheduleSubmit = useScheduledCall(formState.submit);

  const saveChanges = (value: any, { action }: any) => {
    const toPickableValue = (value: PickerValueT) => {
      return value.value;
    };

    const pickableValue = props.isMulti
      ? (value || []).map(toPickableValue)
      : toPickableValue(value);

    formState.setValue(fieldContext.fieldName, pickableValue);
    if (props.submitOnChange) {
      scheduleSubmit();
    }
  };

  const valuePickerProps = {
    ...props,
    pickableValue: formValue,
  };

  return (
    // @ts-ignore
    <ValuePicker
      {...{
        ...valuePickerProps,
        className: cn('ValuePickerField', [props.className]),
      }}
      name={fieldContext.fieldName}
      placeholder={props.placeholder ?? ''}
      noOptionsMessage={() => '...'}
      loadingMessage={() => 'loading...'}
      onChange={saveChanges}
      onKeyDown={(e: any) => {
        if (e.keyCode === 13 && (props.tabOnEnter ?? true)) {
          e.preventDefault();
          tabToNext(e);
        }
        if (props.onKeyDown) {
          props.onKeyDown(e);
        }
      }}
      styles={customStyles}
    ></ValuePicker>
  );
});

const gray = 'hsl(209, 14%, 37%)';
const gray50 = 'hsl(210, 20%, 25%)';
const gray700 = 'hsl(210, 16%, 82%)';
const whitish = 'hsl(214, 15%, 91%)';

export function controlRemoveBorder(state: ObjT) {
  return {
    border: state.isFocused ? 1 : 1,
    // This line disable the blue border
    boxShadow: state.isFocused ? 0 : 0,
    '&:hover': {
      boxShadow: state.isFocused ? 0 : 0,
    },
  };
}

const customStyles = {
  control: (provided: ObjT, state: ObjT) => ({
    ...provided,
    ...controlRemoveBorder(state),
    borderRadius: '8px',
    borderColor: state.isFocused ? whitish : gray,
    borderWidth: '1px',
    border: true,
    backgroundColor: gray,
    padding: '4px',
  }),
  multiValue: (provided: ObjT, state: ObjT) => ({
    ...provided,
    backgroundColor: 'transparent',
  }),
  valueContainer: (provided: ObjT, state: ObjT) => ({
    ...provided,
    caretColor: gray700,
  }),
  multiValueLabel: (provided: ObjT, state: ObjT) => ({
    ...provided,
    paddingLeft: '0px',
    color: gray700,
  }),
  option: (provided: ObjT, state: ObjT) => ({
    ...provided,
    color: gray50,
  }),
  input: (provided: ObjT, state: ObjT) => ({
    ...provided,
    color: gray700,
  }),
  menu: (provided: ObjT, state: ObjT) => ({
    ...provided,
    backgroundColor: gray,
    borderRadius: '8px',
    marginTop: '2px',
  }),
};
