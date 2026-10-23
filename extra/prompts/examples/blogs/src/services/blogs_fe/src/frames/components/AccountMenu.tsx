import { Menu, MenuButton, MenuItem } from '@szhsin/react-menu';
import { observer } from 'mobx-react-lite';
import { withContextProps } from 'react-props-from-context';
import { useSignOut } from '/src/auth/endpoints/mutations/useSignOut';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { authNav } from '/src/auth/routes';
import { Icon } from '/src/frames/components';
import { DialogButtonS } from '/src/frames/components/DialogButton';
import { MenuItemS } from '/src/frames/components/MenuItem';
import { L } from '/src/frames/layout';
import { createContextMenu } from '/src/frames/utils/createContextMenu';
import { navTo } from '/src/routes/navHandler';
import { cn } from '/src/utils/classnames';
import { useBuilder } from '/src/utils/hooks';

// Import styles
import './AccountMenu.scss';
import '/src/frames/components/DialogButton/DialogButton.scss';

export type PropsT = {
  className?: any;
};

const ContextProps = {
  authState: authStateCtx.authState,
};

export const AccountMenu = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const signOut = useSignOut(props.authState).mutateAsync;

    const accountMenu = useBuilder(() => createContextMenu());
    const StyledMenuItem = (props: any) => {
      return (
        <MenuItem
          {...props}
          className={cn(
            L.row.revFlagPole(),
            'min-w-[200px]',
            'bg-transparent',
            'text-gray-800',
            'cursor-pointer'
          )}
        />
      );
    };

    if (!accountMenu.menuProps) {
      return null;
    }

    return (
      <div className={cn('AccountMenu', [props.className])}>
        <Menu
          menuButton={
            <MenuButton
              className={cn(
                'DialogButton',
                [
                  DialogButtonS.color.withTealText(),
                  DialogButtonS.fontSize.medium(),
                ],
                [DialogButtonS.padding.medium(), L.row.skewer()]
              )}
            >
              Account
            </MenuButton>
          }
          className="mt-4 bg-white font-bold"
          transition
        >
          {!props.authState.isAuthenticated && (
            <StyledMenuItem onClick={() => navTo(authNav.signIn({}))}>
              <Icon className={cn(MenuItemS.Icon())} name="signIn" />
              Sign In
            </StyledMenuItem>
          )}
          {props.authState.isAuthenticated && (
            <StyledMenuItem
              onClick={() => {
                signOut({}).then(() => {
                  navTo(authNav.signIn({}));
                });
              }}
            >
              <Icon className={cn(MenuItemS.Icon())} name="signOut" />
              Sign Out
            </StyledMenuItem>
          )}
        </Menu>
      </div>
    );
  }, ContextProps)
);
