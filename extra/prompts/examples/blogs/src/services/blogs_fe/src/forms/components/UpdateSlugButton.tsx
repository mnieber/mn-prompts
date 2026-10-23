import { useFormStateContext } from 'react-form-state-context';
import { useFormFieldContext } from '/src/forms/components/FormFieldContext';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';
import { slugify } from '/src/utils/slugify';

export type PropsT = {
  className?: any;
  tabIndex?: number;
  relatedFieldName: string;
};

export const UpdateSlugButton = (props: PropsT) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  return (
    <button
      tabIndex={props.tabIndex ?? -1}
      className={cn('UpdateSlugButton', [L.row.skewer(), props.className])}
      onClick={() => {
        const newSlug = slugify(formState.values[props.relatedFieldName]);
        if (newSlug) {
          const oldSlug = formState.getValue(fieldContext.fieldName);
          if (oldSlug !== newSlug && oldSlug !== '-') {
            formState.setValue(fieldContext.fieldName, newSlug);
          }
        }
      }}
    >
      update
    </button>
  );
};
