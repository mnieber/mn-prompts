import { trackPromise } from 'mobx-resource-states';
import React from 'react';
import { useObservableQuery } from '/src/api/hooks';
import {
  CreateBlogArgsT,
  useCreateBlog,
} from '/src/api/mutations/useCreateBlog';
import { useGetBlogs } from '/src/api/queries/useGetBlogs';
import { BlogsState } from '/src/blogs/BlogsState';
import { useBuilder } from '/src/utils/hooks/useBuilder';
import { useGraftResourceStatesFromMemo } from '/src/utils/hooks/useGraftResourceStatesFromMemo';
import { ObjT } from '/src/utils/types';

export type PropsT = {};

export const useBlogsState = (props: PropsT) => {
  const graftResourceStatesFromMemo = useGraftResourceStatesFromMemo({});

  // Mutations
  const createBlog = useCreateBlog();

  // Queries
  const getBlogs = useObservableQuery(useGetBlogs(), {
    fetchAsLoad: true,
    debugLabel: 'getBlogs',
  });

  const blogsState = useBuilder(() => {
    const state = new BlogsState({
      //
      getBlogs: () => {
        return graftResourceStatesFromMemo({
          resources: getBlogs.data?.blogs ?? [],
        });
      },
      //
      saveBlog: (values: ObjT) => {
        const mutation = createBlog;
        return trackPromise({
          name: 'saveBlog',
          promise: mutation.mutateAsync({
            createBlogForm: values.blogForm,
          } as CreateBlogArgsT),
        }).result;
      },
    });

    return state;
  }) as BlogsState;

  React.useEffect(() => () => blogsState.destroy(), [blogsState]);

  return {
    blogsState,
    getBlogs,
  };
};
