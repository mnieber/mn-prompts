import { FormField, FormFieldS } from '/src/forms/components/FormField';
import { useFieldProps } from '/src/forms/hooks';
import { cn } from '/src/utils/classnames';

type PropsT = { placeholder?: string; className?: any };

export const PasswordField = (props: PropsT) => {
  const fieldProps = useFieldProps({
    fieldType: 'password',
    autoSelect: true,
  });
  return (
    <FormField className={cn('PasswordField', [props.className])}>
      <input
        placeholder={props.placeholder}
        {...fieldProps}
        className={FormFieldS.Input()}
      />
    </FormField>
  );
};
