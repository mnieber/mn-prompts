import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import { withContextProps } from 'react-props-from-context';
import { DeleteBlogPostsErrorT } from '/src/api/mutations/useDeleteBlogPosts';
import { getFailureMessage } from '/src/api/utils/getFailureMessage';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { DeleteSelectionResultT } from '/src/blogPosts/BlogPostsState/facets/BlogPostsDeletion';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { blogsNav } from '/src/blogs/routes';
import { isBlogOwner } from '/src/blogs/utils/isBlogOwner';
import { ActionButton } from '/src/frames/components/ActionButton/ActionButton';
import { errorBannerState } from '/src/frames/errorBannerState';
import { navTo } from '/src/routes/navHandler';
import { cn } from '/src/utils/classnames';

// Import styles
import './DeleteBlogPostsButton.scss';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  authState: authStateCtx.authState,
  blog: blogsCtx.blog,
  blogPosts: blogPostsCtx.blogPosts,
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
  blogPostsDeletion: blogPostsCtx.blogPostsDeletion,
  blogPostsEdit: blogPostsCtx.blogPostsEdit,
  blogPostsSelection: blogPostsCtx.blogPostsSelection,
};

const getDeleteFailureMessage = (error: DeleteBlogPostsErrorT): string => {
  switch (error.code) {
    case 'BLOG_POSTS_NOT_FOUND':
      return 'Some of these blog posts no longer exist. Nothing was deleted.';
    case 'UNEXPECTED':
      return getFailureMessage(error.cause);
  }
};

export const DeleteBlogPostsButton = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const disabled =
      props.blogPostsSelection.items.length === 0 ||
      props.blogPostsAddition.item ||
      props.blogPostsEdit.isEditing ||
      isUpdating(props.blogPosts) ||
      !isBlogOwner(props.blog, props.authState);

    const handleClick = () => {
      const blogSlug = props.blog.slug;
      errorBannerState.clear();
      props.blogPostsDeletion
        .deleteSelection()
        .then(({ result, isHighlightDeleted }: DeleteSelectionResultT) => {
          if (!result.ok) {
            errorBannerState.show(getDeleteFailureMessage(result.error));
            return;
          }
          if (isHighlightDeleted) {
            navTo(blogsNav.blog({ blogSlug }));
          }
        });
    };

    return (
      <ActionButton
        disabled={disabled}
        danger={true}
        className={cn('DeleteBlogPostsButton', props.className)}
        onClick={handleClick}
        label="Delete selected blog posts"
      />
    );
  }, ContextProps)
);
