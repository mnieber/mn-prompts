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
    // @ts-expect-error TS loses isMulti, isCreatable and labelFromValue in the spread of the generic props
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

const ink = 'hsl(215, 28%, 17%)';
const canvas = 'hsl(210, 25%, 96%)';
const line = 'hsl(212, 22%, 89%)';
const accent = 'hsl(14, 88%, 44%)';
const accentSoft = 'hsl(18, 100%, 96%)';

const customStyles = {
  control: (provided: ObjT, state: ObjT) => ({
    ...provided,
    borderRadius: '8px',
    borderColor: state.isFocused ? accent : line,
    borderWidth: '1px',
    boxShadow: 'none',
    backgroundColor: 'white',
    fontSize: '14px',
    '&:hover': {
      borderColor: state.isFocused ? accent : line,
    },
  }),
  multiValue: (provided: ObjT, state: ObjT) => ({
    ...provided,
    backgroundColor: canvas,
  }),
  valueContainer: (provided: ObjT, state: ObjT) => ({
    ...provided,
    caretColor: ink,
  }),
  multiValueLabel: (provided: ObjT, state: ObjT) => ({
    ...provided,
    color: ink,
  }),
  singleValue: (provided: ObjT, state: ObjT) => ({
    ...provided,
    color: ink,
  }),
  option: (provided: ObjT, state: ObjT) => ({
    ...provided,
    fontSize: '14px',
    color: state.isSelected ? accent : ink,
    fontWeight: state.isSelected ? 600 : 400,
    backgroundColor: state.isSelected
      ? accentSoft
      : state.isFocused
      ? canvas
      : 'white',
    '&:active': {
      backgroundColor: accentSoft,
    },
  }),
  input: (provided: ObjT, state: ObjT) => ({
    ...provided,
    color: ink,
  }),
  menu: (provided: ObjT, state: ObjT) => ({
    ...provided,
    backgroundColor: 'white',
    border: `1px solid ${line}`,
    borderRadius: '8px',
    boxShadow: '0 4px 12px hsla(215, 28%, 17%, 0.1)',
    marginTop: '4px',
    overflow: 'hidden',
  }),
};
