import React from 'react';

export type FormFieldContextPropsT = {
  fieldName: string;
  submitOnEnter?: boolean;
  tabOnEnter?: boolean;
};

const getNullFormFieldContext = (): FormFieldContextPropsT => {
  return {
    fieldName: '',
    submitOnEnter: false,
    tabOnEnter: false,
  };
};

const Context = React.createContext(getNullFormFieldContext());

export const FormFieldContext = (
  props: React.PropsWithChildren<FormFieldContextPropsT>
) => {
  const { children, ...contextProps } = props;

  return <Context.Provider value={contextProps}>{children}</Context.Provider>;
};

export const useFormFieldContext = (): FormFieldContextPropsT => {
  return React.useContext(Context);
};
