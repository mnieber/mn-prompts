import { observer } from 'mobx-react-lite';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { Route, Switch } from 'wouter';
import { RequireSignInEffect } from '/src/auth/components/RequireSignInEffect';
import { BlogPostListView } from '/src/blogPosts/components';
import { BlogPostFormView } from '/src/blogPosts/components/BlogPostFormView';
import { CreateBlogPostButton } from '/src/blogPosts/components/CreateBlogPostButton';
import { CreateBlogPostEffect } from '/src/blogPosts/components/CreateBlogPostEffect';
import { DeleteBlogPostsButton } from '/src/blogPosts/components/DeleteBlogPostsButton';
import { EditBlogPostButton } from '/src/blogPosts/components/EditBlogPostButton';
import { MarkBlogPostAsPublishedButton } from '/src/blogPosts/components/MarkBlogPostAsPublishedButton';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { blogPostsRoutes } from '/src/blogPosts/routes';
import { BlogListView, SelectBlogEffect } from '/src/blogs/components';
import { BlogFormView } from '/src/blogs/components/BlogFormView';
import { CreateBlogEffect } from '/src/blogs/components/CreateBlogEffect';
import { SelectBlogPostEffect } from '/src/blogs/components/SelectBlogPostEffect';
import { blogsRoutes } from '/src/blogs/routes';
import { CardS } from '/src/frames/components/Card';
import { ext } from '/src/routes/navHandler';
import { cn } from '/src/utils/classnames';

// Import styles
import './BlogsPage.scss';

export const ContextProps = {
  //
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
  blogPostsEdit: blogPostsCtx.blogPostsEdit,
};

export type PropsT = React.PropsWithChildren<{
  className?: any;
}>;

export const BlogsPage = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const showBlogPostForm =
      props.blogPostsEdit.isEditing || props.blogPostsAddition.item;

    return (
      <div className={cn('BlogsPage', props.className)}>
        {
          // 🔳 LeftSideBar
        }
        <div className={cn('BlogsPage__LeftSideBar', CardS.color.surface())}>
          <div className={cn('BlogsPage__LeftSideBarTitle')}>Blogs</div>
          <BlogListView className={cn()} />
        </div>
        {
          // 🔳 RightCanvas
        }
        <div className={cn('BlogsPage__RightCanvas')}>
          <Switch>
            <Route path={blogsRoutes.createBlog()}>
              <RequireSignInEffect />
              <CreateBlogEffect />
              <BlogFormView className="grow-0" />
            </Route>
            <Route path={ext(blogsRoutes.blogs())}>
              <Route path={ext(blogsRoutes.blog())}>
                <SelectBlogEffect />
                <div className={cn('BlogsPage__Toolbar')}>
                  <CreateBlogPostButton className="mr-auto" />
                  <EditBlogPostButton />
                  <MarkBlogPostAsPublishedButton />
                  <DeleteBlogPostsButton />
                </div>
                <BlogPostListView className="grow-0" />
                <Route path={blogPostsRoutes.blogPost()}>
                  <SelectBlogPostEffect />
                </Route>
                <Route path={blogPostsRoutes.createBlogPost()}>
                  <RequireSignInEffect />
                  <CreateBlogPostEffect />
                </Route>
                {showBlogPostForm && <BlogPostFormView className="grow-0" />}
              </Route>
            </Route>
          </Switch>
        </div>
      </div>
    );
  }, ContextProps)
);

export const BlogsPageS = {};
