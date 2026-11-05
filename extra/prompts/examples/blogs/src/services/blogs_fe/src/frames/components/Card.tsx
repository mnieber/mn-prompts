import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './Card.scss';

export const CardS = {
  root: () => cn('Card', L.col.banner()),
  color: {
    surface: () => 'border border-line bg-surface shadow-sm',
  },
  size: { medium: () => cn('py-[18px] px-4') },
};
