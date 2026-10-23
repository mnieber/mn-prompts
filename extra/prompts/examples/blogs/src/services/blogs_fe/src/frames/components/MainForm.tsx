import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// A MainForm has:
// - a GlobalError. This component shows an error message with some space below it.
//   Note: if there is no global error, then no error - or space - is shown.
// - one or more Fields. A field is a wrapper around the form-field label, the form-field
//   and the form-field-error.
// - a Buttons container (optional, if there is more than one button).
// - one or more Button components. E.g. a 'Save Clip' button.
export const MainFormS = {
  root: {
    padding: {
      default: () => 'p-4',
    },
  },
  GlobalError: () => 'mb-4',
  Field: () => 'mb-6',
  Buttons: () => cn([L.row.skewer(), 'self-end']),
  Button: {
    root: () => '',
    gap: () => 'mr-2',
  },
};
