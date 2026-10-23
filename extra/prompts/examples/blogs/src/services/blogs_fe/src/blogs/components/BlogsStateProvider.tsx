import { makeAutoObservable } from 'mobx';
import { observer } from 'mobx-react-lite';
import { updateSources } from 'mobx-resource-states';
import React from 'react';
import { isQueryLoading } from '/src/api/lib/ObservableQuery';
import { BlogsContext } from '/src/blogs/hooks/useBlogsContext';
import { useBlogsState } from '/src/blogs/hooks/useBlogsState';
import { createGetProps } from '/src/utils/createGetProps';
import { useBuilder } from '/src/utils/hooks/useBuilder';

export type PropsT = React.PropsWithChildren<{}>;

export const BlogsStateProvider = observer((props: PropsT) => {
  const { blogsState, getBlogs } = useBlogsState({});

  const cache = useBuilder(() =>
    makeAutoObservable({
      get blog() {
        return updateSources(
          {
            resource: blogsState.blogsCtr.highlight.item,
            resourceName: 'blog',
          },
          ['loading', () => isQueryLoading(getBlogs), 'blog']
        );
      },
      get blogs() {
        return updateSources({ resource: blogsState.blogsCtr.data.blogs }, [
          'loading',
          () => isQueryLoading(getBlogs),
          'getBlogs',
        ]);
      },
    })
  );

  const getBlogsContext = () => {
    return createGetProps({
      blogsState: () => blogsState,
      blogs: () => cache.blogs,
      blog: () => cache.blog,
      blogsAddition: () => blogsState.blogsCtr.addition,
      blogsEdit: () => blogsState.blogsCtr.edit,
      blogsHighlight: () => blogsState.blogsCtr.highlight,
      blogsSelection: () => blogsState.blogsCtr.selection,
    });
  };

  return (
    <BlogsContext.Provider value={getBlogsContext()}>
      {props.children}
    </BlogsContext.Provider>
  );
});
