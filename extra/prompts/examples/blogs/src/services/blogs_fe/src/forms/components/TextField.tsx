import { FormField, FormFieldS } from '/src/forms/components/FormField';
import { FieldPropsT, useFieldProps } from '/src/forms/hooks';
import { cn } from '/src/utils/classnames';

// Import styles
import './TextField.scss';

export type PropsT = Partial<FieldPropsT> & {
  placeholder?: string;
  className?: any;
};

export const TextField = (props: PropsT) => {
  const fieldProps = useFieldProps({
    ...props,
    fieldType: props.fieldType ?? 'text',
  });

  return (
    <FormField className={cn('TextField', [props.className])}>
      <input
        placeholder={props.placeholder}
        {...fieldProps}
        className={FormFieldS.Input()}
      />
    </FormField>
  );
};
