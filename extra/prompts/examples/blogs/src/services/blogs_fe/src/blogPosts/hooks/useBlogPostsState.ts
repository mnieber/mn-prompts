import { trackPromise } from 'mobx-resource-states';
import React from 'react';
import { Highlight } from 'skandha-facets';
import { useDeleteBlogPosts } from '/src/api/endpoints';
import { useObservableQuery } from '/src/api/hooks';
import { DeleteBlogPostsArgsT, useGetBlogTags } from '/src/api/mutations';
import {
  CreateBlogPostArgsT,
  useCreateBlogPost,
} from '/src/api/mutations/useCreateBlogPost';
import { useMarkBlogPostAsPublished } from '/src/api/mutations/useMarkBlogPostAsPublished';
import {
  UpdateBlogPostArgsT,
  useUpdateBlogPost,
} from '/src/api/mutations/useUpdateBlogPost';
import { useGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { BlogT } from '/src/api/types/BlogT';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';
import { useBuilder } from '/src/utils/hooks/useBuilder';
import { useGraftResourceStatesFromMemo } from '/src/utils/hooks/useGraftResourceStatesFromMemo';
import { lookUp } from '/src/utils/ids';
import { ObjT } from '/src/utils/types';
import { toPickerValue } from '/src/utils/valuePicker';

export type PropsT = {
  getBlog: () => BlogT | undefined;
};

export const useBlogPostsState = (props: PropsT) => {
  const graftResourceStatesFromMemo = useGraftResourceStatesFromMemo({});

  // Mutations
  const deleteBlogPosts = useDeleteBlogPosts();
  const createBlogPost = useCreateBlogPost();
  const updateBlogPost = useUpdateBlogPost();
  const blogPostsHighlightRef = React.useRef<Highlight | undefined>();
  const markBlogPostAsPublished = useMarkBlogPostAsPublished();

  // Queries
  const getBlogPosts = useObservableQuery(
    useGetBlogPosts(
      { blogSlug: props.getBlog()?.slug ?? '' },
      { enabled: !!props.getBlog() }
    ),
    {
      fetchAsLoad: true,
      debugLabel: 'getBlogPosts',
    }
  );
  const getBlogTags = useGetBlogTags();

  const loadBlogTagsOptions = (inputValue: string) => {
    return getBlogTags.mutateAsync({ inputValue }).then((response: ObjT) => {
      return response.tags.map(toPickerValue);
    });
  };

  const blogPostsState = useBuilder(() => {
    const state = new BlogPostsState({
      //
      getBlogPosts: () => {
        return graftResourceStatesFromMemo({
          resources: getBlogPosts.data?.blogPosts ?? [],
        });
      },
      //
      saveBlogPost: (values: ObjT) => {
        if (values.blogPostForm.isTransient) {
          return trackPromise({
            name: 'createBlogPost',
            promise: createBlogPost.mutateAsync({
              blog: props.getBlog(),
              blogPost: blogPostsHighlightRef.current?.item,
              createBlogPostForm: values.blogPostForm,
            } as CreateBlogPostArgsT),
          }).result;
        } else {
          return trackPromise({
            name: 'saveBlogPost',
            promise: updateBlogPost.mutateAsync({
              blog: props.getBlog(),
              blogPost: blogPostsHighlightRef.current?.item,
              updateBlogPostForm: values.blogPostForm,
            } as UpdateBlogPostArgsT),
          }).result;
        }
      },
      //
      deleteBlogPosts: (ids: string[]) => {
        const blogPosts = lookUp(
          ids,
          blogPostsState.blogPostsCtr.data.blogPostById
        );
        return trackPromise({
          name: 'deleteBlogPosts',
          states: { updating: blogPosts },
          promise: deleteBlogPosts.mutateAsync({
            blog: props.getBlog(),
            blogPostIds: ids,
          } as DeleteBlogPostsArgsT),
        }).result;
      },
      //
      markBlogPostAsPublished: (blogPostId: string) => {
        const blog = props.getBlog();
        if (!blog) {
          throw new Error('Blog not found');
        }
        return trackPromise({
          name: 'markBlogPostAsPublished',
          promise: markBlogPostAsPublished.mutateAsync({
            blog,
            blogPostId,
          }),
        }).result;
      },
    });

    return state;
  }) as BlogPostsState;

  blogPostsHighlightRef.current = blogPostsState.blogPostsCtr.highlight;

  React.useEffect(() => () => blogPostsState.destroy(), [blogPostsState]);

  return {
    blogPostsState,
    getBlogPosts,
    deleteBlogPosts,
    markBlogPostAsPublished,
    loadBlogTagsOptions,
  };
};
