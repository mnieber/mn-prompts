import { Edit } from 'skandha-facets';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';

export class BlogPostsEdit extends Edit {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected saveItem(args: { values: any }) {
    return this.state.props.saveBlogPost(args.values).then((result) => {
      if (result.ok) {
        this.state.blogPostsCtr.addition.confirm();
        this.reset();
      }
      return result;
    });
  }

  protected onCancel(): void {
    this.state.blogPostsCtr.addition.cancel();
  }
}
