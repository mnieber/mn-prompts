import { observer } from 'mobx-react-lite';
import { isLoading } from 'mobx-resource-states';
import { withContextProps } from 'react-props-from-context';
import { BlogT } from '/src/api/types';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { BlogListViewItem } from '/src/blogs/components';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { blogsNav } from '/src/blogs/routes';
import { LoaderBar } from '/src/frames/components/LoaderBar';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

// Import styles
import './BlogListView.scss';

export type PropsT = {
  className?: any;
};

const ContextProps = {
  blogs: blogsCtx.blogs,
  blogsAddition: blogsCtx.blogsAddition,
  blogsEdit: blogsCtx.blogsEdit,
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
  blogPostsEdit: blogPostsCtx.blogPostsEdit,
  blogsSelection: blogsCtx.blogsSelection,
  blogsHighlight: blogsCtx.blogsHighlight,
};

export const BlogListView = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    if (isLoading(props.blogs)) {
      return <BlogListViewLoader className="px-3 py-1" />;
    }

    // While a form is open, the list ignores clicks
    const isInert =
      props.blogsEdit.isEditing ||
      !!props.blogsAddition.item ||
      props.blogPostsEdit.isEditing ||
      !!props.blogPostsAddition.item;

    const blogDivs = props.blogs.map((blog: BlogT) => {
      const url = blogsNav.blog({ blogSlug: blog.slug }).url;
      return (
        <BlogListViewItem
          key={blog.id}
          className={{
            'BlogListViewItem--selected': props.blogsSelection.itemIds.includes(
              blog.id
            ),
            'BlogListViewItem--highlighted':
              props.blogsHighlight.itemId === blog.id,
          }}
          blog={blog}
          url={url}
          isInert={isInert}
        />
      );
    });

    return (
      <div
        className={cn('BlogListView', { 'BlogListView--inert': isInert }, [
          L.col.banner(),
          props.className,
        ])}
        tabIndex={1}
      >
        {blogDivs}
      </div>
    );
  }, ContextProps)
);

export const BlogListViewLoader = (props: { className?: any }) => {
  const loaderBars = ['1', '2', '3'].map((id: string) => {
    return <LoaderBar key={`item-${id}`} className={cn('my-1 h-6')} />;
  });

  return (
    <div
      className={cn('BlogListViewLoader', [
        L.col.banner(),
        'min-w-[50px]',
        props.className,
      ])}
    >
      {loaderBars}
    </div>
  );
};
