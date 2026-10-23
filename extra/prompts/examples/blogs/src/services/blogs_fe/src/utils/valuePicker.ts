export const labelFromValue = (x: any) => x;

export const toPickerValue = (pickableVal: any) => {
  return pickableVal.__isNew__
    ? pickableVal
    : {
        value: pickableVal,
        label: labelFromValue(pickableVal),
      };
};

export const filterValues = (tags: string[], inputValue: string) => {
  return (tags ?? [])
    .map(toPickerValue)
    .filter((i) => i.label.toLowerCase().includes(inputValue.toLowerCase()));
};
