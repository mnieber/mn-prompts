import { observer } from 'mobx-react-lite';
import { isNil } from 'ramda';
import Select from 'react-select';
import AsyncSelect from 'react-select/async';
import AsyncCreatableSelect from 'react-select/async-creatable';
import CreatableSelect from 'react-select/creatable';

export type LoadValuePickerOptionsT<ValueT> = (
  inputValue: string,
  callback: (options: any) => void
) => Promise<ValueT[]>;

export interface PickerValueT {
  value: any;
  label: string;
  __isNew__?: boolean;
}

export type PropsT<ValueT> = {
  isMulti: boolean;
  isCreatable: boolean;
  isAsync?: boolean;
  loadOptions?: LoadValuePickerOptionsT<ValueT>;
  pickableValue?: ValueT | ValueT[];
  labelFromValue: (value: any) => string;
  labelFromPickedValue?: (value: any) => string;
  placeholder?: string;
  [k: string]: any;
  className?: any;
};

export const ValuePicker = observer(
  <ValueT, ConcretePropsT extends PropsT<ValueT>>(
    props: ConcretePropsT
  ): JSX.Element => {
    const {
      isMulti,
      isAsync,
      isCreatable,
      pickableValue,
      loadOptions,
      labelFromValue,
      labelFromPickedValue,
      placeholder,
      ...others
    } = props;

    const toPickedValue = (pickableVal: any) => {
      return pickableVal.__isNew__
        ? pickableVal
        : {
            value: pickableVal,
            label: (labelFromPickedValue ?? labelFromValue)(pickableVal),
          };
    };

    const pickerProps = {
      isMulti: isMulti,
      loadOptions,
      value: isNil(pickableValue)
        ? null
        : isMulti
        ? (pickableValue as any).map(toPickedValue)
        : toPickedValue(pickableValue),
      placeholder: placeholder ?? 'Select...',
      onKeyDown: (e: any) => {
        if (others.onKeyDown) {
          others.onKeyDown(e);
        }
      },
      ...others,
      className: undefined,
    };

    const picker =
      isAsync ?? true ? (
        isCreatable ? (
          <AsyncCreatableSelect {...pickerProps} />
        ) : (
          <AsyncSelect {...pickerProps} />
        )
      ) : isCreatable ? (
        <CreatableSelect {...pickerProps} />
      ) : (
        <Select {...pickerProps} />
      );

    return (
      <div className={props.className} style={{ zIndex: others.zIndex }}>
        {picker}
      </div>
    );
  }
);
