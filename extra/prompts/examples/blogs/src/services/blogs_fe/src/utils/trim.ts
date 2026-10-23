import * as R from 'ramda';
import { cn } from '/src/utils/classnames';
import { ObjT, RecursivePartial } from '/src/utils/types';

const modeCnSymbol = Symbol('modeClassnames');
const overlayResultSymbol = Symbol('overlayedMode');

export type ModeT<TrimT extends ObjT> = TrimT['base'];
export type ModeOverlayT<TrimT extends ObjT> = RecursivePartial<ModeT<TrimT>>;

export type ModeOverlayMapT<TrimT extends ObjT> = {
  [modeName: string]: ModeOverlayT<TrimT>;
};

export function createTrim<BaseTrimT extends ObjT, OverlayTrimT extends ObjT>(
  trim: BaseTrimT,
  overlay: OverlayTrimT
): BaseTrimT & OverlayTrimT {
  return R.mergeDeepRight(trim, overlay) as unknown as BaseTrimT & OverlayTrimT;
}

export const getModeCn = <T extends ObjT>(props?: T) => {
  if (!props) {
    return undefined;
  }

  if (!(props as any)[modeCnSymbol]) {
    (props as any)[modeCnSymbol] = cn(R.values(props ?? {}));
  }
  return (props as any)[modeCnSymbol];
};

export function getMode<TrimT extends ObjT>(
  trim: TrimT,
  flags: ObjT
): ModeT<TrimT> {
  for (const [modeName, isInMode] of Object.entries(flags)) {
    if (isInMode) {
      return overlayMode(trim, modeName);
    }
  }
  return trim.base;
}

export function overlayMode<TrimT extends ObjT>(
  modeOverlayMap: ModeOverlayMapT<TrimT>,
  modeName: string
): ModeT<TrimT> {
  const overlay = (modeOverlayMap[modeName] = modeOverlayMap[modeName] ?? {});
  if (!(overlay as any)[overlayResultSymbol]) {
    (overlay as any)[overlayResultSymbol] = R.mergeDeepRight(
      modeOverlayMap.base,
      overlay
    );
  }
  return (overlay as any)[overlayResultSymbol];
}

export const inlineTrim = (condition: boolean | undefined, trim: ObjT) => {
  return condition ? R.values(trim) : undefined;
};
