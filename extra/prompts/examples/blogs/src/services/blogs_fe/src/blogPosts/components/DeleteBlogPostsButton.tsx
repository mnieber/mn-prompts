import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import { withContextProps } from 'react-props-from-context';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { ActionButton } from '/src/frames/components/ActionButton/ActionButton';
import { cn } from '/src/utils/classnames';

// Import styles
import './DeleteBlogPostsButton.scss';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  authState: authStateCtx.authState,
  blogPosts: blogPostsCtx.blogPosts,
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
  blogPostsDeletion: blogPostsCtx.blogPostsDeletion,
  blogPostsSelection: blogPostsCtx.blogPostsSelection,
};

export const DeleteBlogPostsButton = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const disabled =
      props.blogPostsSelection.items.length === 0 ||
      props.blogPostsAddition.item ||
      isUpdating(props.blogPosts) ||
      !props.authState.isAuthenticated;

    return (
      <ActionButton
        disabled={disabled}
        danger={true}
        className={cn('DeleteBlogPostsButton', props.className)}
        onClick={() =>
          props.blogPostsDeletion.delete({
            itemIds: props.blogPostsSelection.itemIds,
          })
        }
        label="Delete selected blog posts"
      />
    );
  }, ContextProps)
);
