import * as R from 'ramda';
import { data } from 'skandha';
import { BlogPostT } from '/src/api/types';

export class BlogPostsData {
  static className = () => 'BlogPostsData';

  @data blogPosts: BlogPostT[] = [];

  @data get blogPostById() {
    return R.indexBy(R.prop('id'), this.blogPosts);
  }
}
