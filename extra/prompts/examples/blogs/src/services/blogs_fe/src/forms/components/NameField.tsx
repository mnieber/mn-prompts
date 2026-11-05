import { TextField } from '/src/forms/components/TextField';
import { FieldPropsT } from '/src/forms/hooks';

type PropsT = Partial<FieldPropsT> & {
  className?: any;
};

export const NameField = (props: PropsT) => {
  return <TextField {...props} />;
};
