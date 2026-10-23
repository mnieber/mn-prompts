import { Deletion } from 'skandha-facets';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';

export class BlogPostsDeletion extends Deletion {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected deleteItems(args: {
    itemIds: string[];
    moveToTrash?: boolean;
  }): any {
    return this.state.props.deleteBlogPosts(args.itemIds);
  }
}
