# Skill: fe-add-trimmed-component

Applies when writing a component that supports a **trim** — a structured styling interface that lets callers choose from a menu of pre-composed style choices rather than passing raw Tailwind classes. Trims are used for shared UI primitives (buttons, cards, badges) where appearance needs to vary across contexts in a controlled, type-safe way.

---

## File structure

```
frames/components/<Name>/
  <Name>.tsx      ← component; accepts trim prop
  <Name>.scss     ← intrinsic styles
  trim.ts         ← TrimT type + style-object (S) + DefaultTrim
  trims.ts        ← pre-made trim variants built with createTrim
  index.tsx       ← barrel re-export
```

Primary reference: `blogs_fe/src/frames/components/DialogButton/`

---

## 1. `trim.ts` — type, style-object, default trim

```ts
import { ModeOverlayT } from '/src/utils/trim';

// The trim type — declares every slot the component can be styled through.
export type DialogButtonTrimT = {
  base: {
    componentName: string;   // CSS class that identifies which trim variant is active
    root: {
      border: any;
      color: any;
      fontSize: any;
      padding: any;
    };
    Icon: {
      margin: any;
      size: any;
      color: any;
    };
  };
  danger?: ModeOverlayT<DialogButtonTrimT>;    // optional mode overlay
  disabled?: ModeOverlayT<DialogButtonTrimT>;  // optional mode overlay
};

// The style-object — a menu of named Tailwind class strings for each slot.
// Callers pick entries from S to fill the slots of a trim object.
export const DialogButtonS = {
  color: {
    blueWithDarkText: () => 'bg-blue-400 text-blue-darkest hover:bg-blue-600',
    tealWithDarkText: () => 'bg-teal-400 text-teal-darkest hover:bg-teal-600',
    disabled: () => 'text-gray-400 hover:text-gray-400 border-gray-400',
    // ...
  },
  border: {
    none: () => '',
  },
  fontSize: {
    medium: () => 'text-base',
  },
  padding: {
    medium: () => 'px-4 py-2',
  },
};

// The default trim — a concrete trim object using the style-object entries.
// Components use this when the caller does not pass a trim prop.
export const DefaultDialogButtonTrim: DialogButtonTrimT = {
  base: {
    componentName: 'Default',
    root: {
      color: DialogButtonS.color.blueWithDarkText(),
      border: DialogButtonS.border.none(),
      fontSize: DialogButtonS.fontSize.medium(),
      padding: DialogButtonS.padding.medium(),
    },
    Icon: { margin: '...', size: '...', color: '...' },
  },
  danger: undefined,
  disabled: {
    root: { color: DialogButtonS.color.disabled() },
  },
};
```

### Key rules for `trim.ts`

- **`TrimT` type** — declare a named type (ending in `T`) that describes every styleable slot. All leaf values are typed `any` to stay flexible.
- **Mode overlays** — `danger?` and `disabled?` are optional `ModeOverlayT<TrimT>` entries. `ModeOverlayT` is a deep partial of the trim type; only the overridden slots need to be specified.
- **Style-object (`S`)** — export a style-object (name pattern: `<Name>S`) with named functions that return Tailwind class strings. This creates a vocabulary callers can use to fill trim slots without writing raw strings.
- **`DefaultTrim`** — export one concrete default trim. Components fall back to this when `props.trim` is not provided.

---

## 2. `trims.ts` — pre-made variants

```ts
import { DefaultDialogButtonTrim, DialogButtonS, type DialogButtonTrimT } from '/src/frames/components/DialogButton';
import { createTrim } from '/src/utils/trim';

export const BlueDialogButtonTrim: DialogButtonTrimT = createTrim(
  DefaultDialogButtonTrim,
  {
    base: {
      componentName: 'Blue-DialogButton',
      root: {
        color: DialogButtonS.color.blueWithDarkText(),
      },
    },
    disabled: {
      root: { color: DialogButtonS.color.disabled() },
    },
  }
);

export const TealDialogButtonTrim: DialogButtonTrimT = createTrim(
  DefaultDialogButtonTrim,
  {
    base: {
      componentName: 'Teal-DialogButton',
      root: { color: DialogButtonS.color.tealWithDarkText() },
    },
  }
);
```

### Key rules for `trims.ts`

- **`createTrim(base, overrides)`** — deep-merges `overrides` onto `base`. Import from `/src/utils/trim`.
- Each variant is a named export typed as `XxxTrimT`.
- `componentName` identifies which variant is active (used as a CSS class on the root element for debugging and SCSS targeting).

---

## 3. `<Name>.tsx` — the component

```tsx
import { DefaultDialogButtonTrim, DialogButtonTrimT } from '/src/frames/components/DialogButton/trim';
import { getMode, getModeCn } from '/src/utils/trim';
import { cn } from '/src/utils/classnames';
import './DialogButton.scss';

export type PropsT = {
  trim?: DialogButtonTrimT;
  disabled?: boolean;
  label: string;
  className?: any;
} & ButtonPropsT;

export const DialogButton = (props: PropsT) => {
  const trim = props.trim ?? DefaultDialogButtonTrim;
  const mode = getMode(trim, {
    danger: props.danger && !props.disabled,
    disabled: props.disabled,
  });

  return (
    <button
      disabled={props.disabled}
      className={cn(
        trim.base.componentName,   // variant identifier class
        'DialogButton',
        [
          getModeCn(mode.root),    // merged root styles for the active mode
          'select-none',
        ],
        props.className
      )}
      {...rest}
    >
      {props.label}
    </button>
  );
};
```

### Key rules for the component

- **`trim` prop is optional** — default to `DefaultTrim` when not provided.
- **`getMode(trim, flags)`** — computes the active mode by merging the relevant mode overlays onto `trim.base`. Import from `/src/utils/trim`.
- **`getModeCn(mode.slotName)`** — returns the class string for a given slot in the resolved mode. Use this instead of accessing `trim.base.root.color` directly so that mode overlays are applied.
- **`trim.base.componentName`** — always apply as a CSS class so the active variant is visible in DevTools.
- Props are not destructured — access via `props.foo`.

---

## When to use trims

Trims are appropriate for shared primitives that:
- Appear in multiple places with different visual styles
- Need more control than a single `variant` prop provides
- Are likely to grow new style dimensions over time

For one-off components used in a single context, plain Tailwind via `className` is simpler and preferred.

---

## Checklist

- [ ] `trim.ts`: `TrimT` type with all styleable slots declared as `any`
- [ ] `trim.ts`: style-object (`XxxS`) exports named functions returning Tailwind strings
- [ ] `trim.ts`: `DefaultXxxTrim` exported as a concrete fallback
- [ ] `trim.ts`: mode overlays (`danger?`, `disabled?`) typed as `ModeOverlayT<TrimT>`
- [ ] `trims.ts`: variants built with `createTrim(DefaultTrim, overrides)`; each typed as `XxxTrimT`
- [ ] Component: `trim` prop optional; falls back to `DefaultXxxTrim`
- [ ] Component: `getMode` + `getModeCn` used to resolve active mode styles
- [ ] Component: `trim.base.componentName` applied as CSS class
- [ ] Component: props not destructured
