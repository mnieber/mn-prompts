import { observer } from 'mobx-react-lite';
import { isLoading } from 'mobx-resource-states';
import * as R from 'ramda';
import KeyboardEventHandler from 'react-keyboard-event-handler';
import { withContextProps } from 'react-props-from-context';
import {
  SelectionUIConnector,
  createSelectionKeyHandlers,
} from 'skandha-facets';
import { BlogPostT } from '/src/api/types';
import { BlogPostListViewItem } from '/src/blogPosts/components';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { CardS } from '/src/frames/components/Card';
import { LoaderBar } from '/src/frames/components/LoaderBar';
import { L } from '/src/frames/layout';
import { createKeyDownHandler } from '/src/utils';
import { cn } from '/src/utils/classnames';

// Import styles
import './BlogPostListView.scss';

export type PropsT = {
  className?: any;
};

const ContextProps = {
  blog: blogsCtx.blog,
  blogPosts: blogPostsCtx.blogPosts,
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
  blogPostsEdit: blogPostsCtx.blogPostsEdit,
  blogPostsSelection: blogPostsCtx.blogPostsSelection,
  blogPostsHighlight: blogPostsCtx.blogPostsHighlight,
};

export const BlogPostListView = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    if (isLoading(props.blogPosts)) {
      return <BlogPostListViewLoader />;
    }

    const selectionUIConnector = new SelectionUIConnector({
      selection: props.blogPostsSelection,
    });

    // While the form is open, the list ignores clicks and keys
    const isInert =
      props.blogPostsEdit.isEditing || !!props.blogPostsAddition.item;

    const keyHandlers = isInert
      ? {}
      : createSelectionKeyHandlers(props.blogPostsSelection);

    const blogPostDivs = props.blogPosts.map((blogPost: BlogPostT) => (
      <BlogPostListViewItem
        key={blogPost.id}
        className={{
          'BlogPostListViewItem--selected':
            props.blogPostsSelection.itemIds.includes(blogPost.id),
          'BlogPostListViewItem--highlighted':
            props.blogPostsHighlight.itemId === blogPost.id,
        }}
        blog={props.blog}
        blogPost={blogPost}
        selectionUIProps={selectionUIConnector.handle(blogPost.id)}
        isInert={isInert}
      />
    ));

    return (
      <KeyboardEventHandler
        handleKeys={R.keys(keyHandlers)}
        onKeyEvent={createKeyDownHandler(keyHandlers)}
      >
        <div
          className={cn(
            'BlogPostListView',
            { 'BlogPostListView--inert': isInert },
            [L.col.banner(), CardS.root(), CardS.color.surface()],
            props.className
          )}
          tabIndex={1}
        >
          {blogPostDivs}
        </div>
      </KeyboardEventHandler>
    );
  }, ContextProps)
);

export const BlogPostListViewLoader = (props: { className?: any }) => {
  const loaderBars = ['1', '2', '3'].map((id: string) => {
    return <LoaderBar key={`item-${id}`} className={cn('my-1 h-6')} />;
  });

  return (
    <div
      className={cn('BlogPostListViewLoader', [
        L.col.banner(),
        'min-w-[50px]',
        props.className,
      ])}
    >
      {loaderBars}
    </div>
  );
};
