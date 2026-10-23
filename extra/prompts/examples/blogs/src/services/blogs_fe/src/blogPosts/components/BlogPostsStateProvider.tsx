import { makeAutoObservable } from 'mobx';
import { observer } from 'mobx-react-lite';
import { updateSources } from 'mobx-resource-states';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { isRunning } from '/src/api/lib/ObservableMutation';
import { isQueryLoading } from '/src/api/lib/ObservableQuery';
import { BlogPostsContext } from '/src/blogPosts/hooks/useBlogPostsContext';
import { useBlogPostsState } from '/src/blogPosts/hooks/useBlogPostsState';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { createGetProps } from '/src/utils/createGetProps';
import { useBuilder } from '/src/utils/hooks/useBuilder';

export type PropsT = React.PropsWithChildren<{}>;

const ContextProps = {
  blogsHighlight: blogsCtx.blogsHighlight,
};

export const BlogPostsStateProvider = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const {
      blogPostsState,
      getBlogPosts,
      deleteBlogPosts,
      loadBlogTagsOptions,
    } = useBlogPostsState({ getBlog: () => props.blogsHighlight.item });

    const cache = useBuilder(() =>
      makeAutoObservable({
        get blogPosts() {
          return updateSources(
            { resource: blogPostsState.blogPostsCtr.data.blogPosts },
            ['loading', () => isQueryLoading(getBlogPosts), 'getBlogPosts'],
            ['updating', () => isRunning(deleteBlogPosts), 'deleteBlogPosts']
          );
        },
        get blogPost() {
          return updateSources({
            resource: blogPostsState.blogPostsCtr.highlight.item,
          });
        },
      })
    );

    const getBlogPostsContext = () => {
      return createGetProps({
        blogPostsState: () => blogPostsState,
        blogPostsStateActions: () => blogPostsState.actionsCtr,
        blogPosts: () => cache.blogPosts,
        blogPost: () => cache.blogPost,
        blogPostsAddition: () => blogPostsState.blogPostsCtr.addition,
        blogPostsDeletion: () => blogPostsState.blogPostsCtr.deletion,
        blogPostsEdit: () => blogPostsState.blogPostsCtr.edit,
        blogPostsHighlight: () => blogPostsState.blogPostsCtr.highlight,
        blogPostsSelection: () => blogPostsState.blogPostsCtr.selection,
        loadBlogTagsOptions: () => loadBlogTagsOptions,
      });
    };

    return (
      <BlogPostsContext.Provider value={getBlogPostsContext()}>
        {props.children}
      </BlogPostsContext.Provider>
    );
  }, ContextProps)
);
