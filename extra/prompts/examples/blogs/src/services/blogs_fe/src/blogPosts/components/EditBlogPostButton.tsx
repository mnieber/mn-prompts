import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import { withContextProps } from 'react-props-from-context';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { ActionButton } from '/src/frames/components/ActionButton/ActionButton';
import { cn } from '/src/utils/classnames';

// Import styles
import './EditBlogPostButton.scss';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  authState: authStateCtx.authState,
  blogPost: blogPostsCtx.blogPost,
  blogPostEdit: blogPostsCtx.blogPostsEdit,
};

export const EditBlogPostButton = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const disabled =
      !props.blogPost ||
      isUpdating(props.blogPost) ||
      !props.authState.isAuthenticated;

    return (
      <ActionButton
        disabled={disabled}
        className={cn('EditBlogPostButton', 'my-4', props.className)}
        onClick={() => props.blogPostEdit.enable()}
        label="Edit selected blog post"
      />
    );
  }, ContextProps)
);
