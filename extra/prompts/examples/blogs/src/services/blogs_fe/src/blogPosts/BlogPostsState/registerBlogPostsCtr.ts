import * as R from 'ramda';
import { mapDataToProps } from 'skandha';
import { registerCtr } from 'skandha-mobx';
import { BlogPostT } from '/src/api/types';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';

const mapData = (state: BlogPostsState) => {
  const ctr = state.blogPostsCtr;
  const getBlogPostById = (x: string | undefined) =>
    x ? ctr.data.blogPostById[x] : undefined;

  mapDataToProps(ctr, {
    data: {
      blogPosts: () => state.props.getBlogPosts(),
    },
    selection: {
      selectableIds: () => R.map(R.prop('id'), ctr.data.blogPosts),
      items: () =>
        ctr.selection.itemIds
          .map(getBlogPostById)
          .filter((x?: BlogPostT) => !!x) as BlogPostT[],
    },
    highlight: {
      highlightableIds: () => R.map(R.prop('id'), ctr.data.blogPosts),
      item: () => getBlogPostById(ctr.highlight.itemId),
    },
  });
};

export const registerBlogPostsCtr = (state: BlogPostsState) => {
  registerCtr({
    ctr: state.blogPostsCtr,
    options: { name: 'BlogPostsState.BlogPosts' },
    initCtr: () => {
      mapData(state);
    },
  });
};
