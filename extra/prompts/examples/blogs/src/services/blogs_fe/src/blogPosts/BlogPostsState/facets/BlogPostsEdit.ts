import { Edit } from 'skandha-facets';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';
import { ObjT } from '/src/utils/types';

export class BlogPostsEdit extends Edit {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected saveItem(args: { values: any }): any {
    return this.state.props.saveBlogPost(args.values).then((response: ObjT) => {
      this.state.blogPostsCtr.addition.confirm();
      return response;
    });
  }

  protected onCancel(): void {
    this.state.blogPostsCtr.addition.cancel();
  }
}
