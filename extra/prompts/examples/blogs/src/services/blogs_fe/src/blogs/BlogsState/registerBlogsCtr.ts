import * as R from 'ramda';
import { mapDataToProps } from 'skandha';
import { registerCtr } from 'skandha-mobx';
import { BlogsState } from '/src/blogs/BlogsState';

const mapData = (state: BlogsState) => {
  const ctr = state.blogsCtr;
  const getBlogById = (x: string) => ctr.data.blogById[x];

  mapDataToProps(ctr, {
    data: {
      blogs: () => state.props.getBlogs(),
    },
    selection: {
      selectableIds: () => R.map(R.prop('id'), ctr.data.blogs),
    },
    highlight: {
      item: () =>
        ctr.highlight.itemId ? getBlogById(ctr.highlight.itemId) : undefined,
    },
  });
};

export const registerBlogsCtr = (state: BlogsState) => {
  registerCtr({
    ctr: state.blogsCtr,
    options: { name: 'BlogsState.Blogs' },
    initCtr: () => {
      mapData(state);
    },
  });
};
