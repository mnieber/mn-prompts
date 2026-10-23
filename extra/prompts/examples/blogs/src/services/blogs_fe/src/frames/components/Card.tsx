import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './Card.scss';

export const CardS = {
  root: () => cn('Card', L.col.banner()),
  color: {
    gray: () => 'bg-gray-medium',
  },
  size: { medium: () => cn('py-[18px] px-4') },
};
