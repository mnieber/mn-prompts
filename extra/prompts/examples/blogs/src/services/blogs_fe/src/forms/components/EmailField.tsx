import { FormField, FormFieldS } from '/src/forms/components/FormField';
import { useFieldProps } from '/src/forms/hooks';
import { FieldPropsT } from '/src/forms/hooks/useFieldProps';
import { cn } from '/src/utils/classnames';

type PropsT = Partial<FieldPropsT> & {
  className?: any;
  placeholder?: string;
};

export const EmailField = (props: PropsT) => {
  const fieldProps = useFieldProps({ fieldType: 'text' });

  return (
    <FormField className={cn('EmailField', [props.className])}>
      <input
        placeholder={props.placeholder}
        {...fieldProps}
        className={FormFieldS.Input()}
      />
    </FormField>
  );
};
