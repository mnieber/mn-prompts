import { observer } from 'mobx-react-lite';
import React from 'react';
import {
  FormFieldContext,
  FormFieldContextPropsT,
  FormFieldError,
} from '/src/forms/components';
import { cn } from '/src/utils/classnames';

// Import styles
import './Field.scss';

type PropsT = React.PropsWithChildren<
  FormFieldContextPropsT & {
    className?: any;
  }
>;

export const Field = observer((props: PropsT) => {
  return (
    <FormFieldContext {...props}>
      <div className={cn('Field', ['flex flex-col', props.className])}>
        {props.children}
        <FormFieldError />
      </div>
    </FormFieldContext>
  );
});
