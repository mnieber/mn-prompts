import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import { withContextProps } from 'react-props-from-context';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { ActionButton } from '/src/frames/components/ActionButton/ActionButton';
import { cn } from '/src/utils/classnames';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  authState: authStateCtx.authState,
  blogPost: blogPostsCtx.blogPost,
  blogPostsActions: blogPostsCtx.blogPostsActions,
};

export const MarkBlogPostAsPublishedButton = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const disabled =
      !props.blogPost ||
      isUpdating(props.blogPost) ||
      !props.authState.isAuthenticated ||
      props.blogPost.isPublished;

    const handleClick = () => {
      if (props.blogPost) {
        props.blogPostsActions.markBlogPostAsPublished(props.blogPost.id);
      }
    };

    return (
      <ActionButton
        disabled={disabled}
        className={cn('MarkBlogPostAsPublishedButton', 'my-4', props.className)}
        onClick={handleClick}
        label={
          props.blogPost?.isPublished
            ? 'Already Published'
            : 'Mark as Published'
        }
      />
    );
  }, ContextProps)
);
