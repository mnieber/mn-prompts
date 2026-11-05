import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import { withContextProps } from 'react-props-from-context';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { blogPostsNav } from '/src/blogPosts/routes';
import { isBlogOwner } from '/src/blogs/utils/isBlogOwner';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { ActionButton } from '/src/frames/components/ActionButton/ActionButton';
import { AccentActionButtonTrim } from '/src/frames/components/ActionButton/trims';
import { navStateCtx } from '/src/routes/hooks/useNavStateContext';
import { navTo } from '/src/routes/navHandler';
import { cn } from '/src/utils/classnames';

// Import styles
import './CreateBlogPostButton.scss';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  authState: authStateCtx.authState,
  navState: navStateCtx.navState,
  blog: blogsCtx.blog,
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
  blogPostsEdit: blogPostsCtx.blogPostsEdit,
};

export const CreateBlogPostButton = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const disabled =
      !props.blog ||
      isUpdating(props.blog) ||
      !isBlogOwner(props.blog, props.authState) ||
      props.blogPostsEdit.isEditing ||
      !!props.blogPostsAddition.item;

    return (
      <ActionButton
        trim={AccentActionButtonTrim}
        disabled={disabled}
        className={cn('CreateBlogPostButton', props.className)}
        onClick={() => {
          props.navState.storeNavPoint();
          navTo(blogPostsNav.createBlogPost({ blogSlug: props.blog?.slug }));
        }}
        label="Create blog post"
      />
    );
  }, ContextProps)
);
