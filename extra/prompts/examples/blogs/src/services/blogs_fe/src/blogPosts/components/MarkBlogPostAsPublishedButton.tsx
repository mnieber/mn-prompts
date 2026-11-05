import { observer } from 'mobx-react-lite';
import { isUpdating } from 'mobx-resource-states';
import { withContextProps } from 'react-props-from-context';
import { MarkBlogPostAsPublishedErrorT } from '/src/api/mutations/useMarkBlogPostAsPublished';
import { getFailureMessage } from '/src/api/utils/getFailureMessage';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { isBlogOwner } from '/src/blogs/utils/isBlogOwner';
import { ActionButton } from '/src/frames/components/ActionButton/ActionButton';
import { errorBannerState } from '/src/frames/errorBannerState';
import { cn } from '/src/utils/classnames';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  authState: authStateCtx.authState,
  blog: blogsCtx.blog,
  blogPost: blogPostsCtx.blogPost,
  blogPostsActions: blogPostsCtx.blogPostsActions,
  blogPostsEdit: blogPostsCtx.blogPostsEdit,
};

const getPublishFailureMessage = (
  error: MarkBlogPostAsPublishedErrorT
): string => {
  switch (error.code) {
    case 'UNEXPECTED':
      return getFailureMessage(error.cause);
  }
};

export const MarkBlogPostAsPublishedButton = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const disabled =
      !props.blogPost ||
      isUpdating(props.blogPost) ||
      !isBlogOwner(props.blog, props.authState) ||
      props.blogPostsEdit.isEditing ||
      props.blogPost.isPublished;

    const handleClick = () => {
      if (props.blogPost) {
        errorBannerState.clear();
        props.blogPostsActions
          .markBlogPostAsPublished(props.blogPost.id)
          .then((result) => {
            if (!result.ok) {
              errorBannerState.show(getPublishFailureMessage(result.error));
            }
          });
      }
    };

    return (
      <ActionButton
        disabled={disabled}
        className={cn('MarkBlogPostAsPublishedButton', props.className)}
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
