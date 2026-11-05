import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import { withContextProps } from 'react-props-from-context';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { isBlogOwner } from '/src/blogs/utils/isBlogOwner';
import { ActionButton } from '/src/frames/components/ActionButton/ActionButton';
import { cn } from '/src/utils/classnames';

// Import styles
import './EditBlogPostButton.scss';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  authState: authStateCtx.authState,
  blog: blogsCtx.blog,
  blogPost: blogPostsCtx.blogPost,
  blogPostEdit: blogPostsCtx.blogPostsEdit,
};

export const EditBlogPostButton = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const disabled =
      !props.blogPost ||
      isUpdating(props.blogPost) ||
      !isBlogOwner(props.blog, props.authState);

    return (
      <ActionButton
        disabled={disabled}
        className={cn('EditBlogPostButton', props.className)}
        onClick={() => props.blogPostEdit.enable()}
        label="Edit selected blog post"
      />
    );
  }, ContextProps)
);
