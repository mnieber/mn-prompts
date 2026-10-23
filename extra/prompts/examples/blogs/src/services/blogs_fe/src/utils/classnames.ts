import classnames from 'classnames';

export const cn = classnames;

export const cnn = (...args: any) => {
  return {
    classNames: classnames(...args),
  };
};
