import { useFormFieldContext } from '/src/forms/components';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './FormFieldLabel.MainView.scss';

type PropsT = {
  className?: any;
  label: string;
  buttons?: any[];
};

export const FormFieldLabel = (props: PropsT) => {
  const fieldContext = useFormFieldContext();

  return (
    <div className={cn('FormFieldLabel', [L.row.skewer()])}>
      {props.label && (
        <label
          className={cn('FormFieldLabel__Label', props.className)}
          htmlFor={fieldContext.fieldName}
        >
          {props.label}
        </label>
      )}
      {!!props.buttons?.length && <div className="flex-grow" />}
      {!!props.buttons?.length && (
        <div
          className={cn('FormFieldLabel__Buttons', ['flex flex-row', 'ml-2'])}
        >
          {props.buttons}
        </div>
      )}
    </div>
  );
};
