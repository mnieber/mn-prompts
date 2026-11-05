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
    const signOut = useSignOut(props.authState).run;

    const accountMenu = useBuilder(() => createContextMenu());
    const StyledMenuItem = (props: any) => {
      return (
        <MenuItem
          {...props}
          className={cn('AccountMenu__Item', L.row.skewer())}
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
                  DialogButtonS.color.quiet(),
                  DialogButtonS.fontSize.small(),
                ],
                [DialogButtonS.padding.small(), L.row.skewer()]
              )}
            >
              Account
            </MenuButton>
          }
          menuClassName="AccountMenu__Menu"
          align="end"
          gap={8}
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
