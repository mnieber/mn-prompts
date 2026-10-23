import { action, makeObservable, observable } from 'mobx';

export function createContextMenu() {
  return makeObservable(
    {
      anchorPoint: undefined,
      toggleMenu: function (flag: boolean) {
        console['log']('toggleMenu not initialized');
      },
      menuProps: {},

      init: function (toggleMenu: (flag: boolean) => void, menuProps: any) {
        this.toggleMenu = toggleMenu;
        this.menuProps = menuProps;
      },
      openAtPoint: function (anchorPoint: any) {
        this.anchorPoint = anchorPoint;
        this.toggleMenu(true);
      },
      close: function () {
        this.toggleMenu(false);
      },
    },
    {
      anchorPoint: observable,
      menuProps: observable,
      openAtPoint: action,
      close: action,
      init: action,
    }
  );
}
