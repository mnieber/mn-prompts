export const breakpoints = {
  xs: '320px',
  small: '480px',
  medium: '768px',
  large: '976px',
  xlarge: '1280px',
};

export const L = {
  box: (h: string, w: string) => `flex ${h} ${w}`,
  row: {
    canvas: () => 'flex grow flex-row',
    bar: () => 'flex flex-row',
    skewer: () => 'flex flex-row items-center',
    banner: () => 'flex grow flex-row items-stretch',
    flagPole: () => 'flex flex-row items-start',
    revFlagPole: () => 'flex flex-row items-end',
  },
  col: {
    canvas: () => 'flex grow flex-col',
    bar: () => 'flex flex-col',
    skewer: () => 'flex flex-col items-center',
    banner: () => 'flex grow flex-col items-stretch',
    flagPole: () => 'flex flex-col items-start',
    flagPoleRev: () => 'flex flex-col items-end',
  },
};
