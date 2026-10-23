import * as R from 'ramda';
import { useFormStateContext } from 'react-form-state-context';
import { useFormFieldContext } from '/src/forms/components';
import { TextField } from '/src/forms/components/TextField';
import { FieldPropsT } from '/src/forms/hooks';
import { slugify } from '/src/utils';

type PropsT = Partial<FieldPropsT> & {
  slugFieldName?: string;
  updateSlugField?: boolean;
  className?: any;
};

export const NameField = (props: PropsT) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  const { slugFieldName, ...otherProps } = props;

  return (
    <TextField
      {...otherProps}
      onBlur={() => {
        if (!R.isNil(slugFieldName)) {
          formState.setValue(
            slugFieldName,
            slugify(formState.getValue(fieldContext.fieldName)) + '-'
          );
        }
      }}
    />
  );
};
