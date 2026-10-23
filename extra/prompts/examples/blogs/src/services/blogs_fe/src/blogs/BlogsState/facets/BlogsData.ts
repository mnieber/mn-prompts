import * as R from 'ramda';
import { data } from 'skandha';
import { BlogT } from '/src/api/types';

export class BlogsData {
  static className = () => 'BlogsData';

  @data blogs: BlogT[] = [];

  @data get blogById() {
    return R.indexBy(R.prop('id'), this.blogs);
  }
}
