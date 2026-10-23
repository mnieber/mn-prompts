import * as Skandha from 'skandha';
import { Highlight } from 'skandha-facets';
import { BlogT } from '/src/api/types';
import { BlogsAddition } from '/src/blogs/BlogsState/facets/BlogsAddition';
import { BlogsData } from '/src/blogs/BlogsState/facets/BlogsData';
import { BlogsEdit } from '/src/blogs/BlogsState/facets/BlogsEdit';
import { BlogsSelection } from '/src/blogs/BlogsState/facets/BlogsSelection';
import { registerBlogsCtr } from '/src/blogs/BlogsState/registerBlogsCtr';
import { ObjT } from '/src/utils/types';

export type PropsT = {
  getBlogs: () => BlogT[];
  saveBlog: (values: ObjT) => Promise<any>;
};

export class BlogsState {
  props: PropsT;

  blogsCtr = {
    data: new BlogsData(),
    addition: new BlogsAddition(this),
    edit: new BlogsEdit(this),
    highlight: new Highlight<BlogT>(),
    selection: new BlogsSelection(this),
  };

  destroy() {
    Skandha.cleanUpCtr(this);
  }

  constructor(props: PropsT) {
    this.props = props;
    registerBlogsCtr(this);
  }
}
