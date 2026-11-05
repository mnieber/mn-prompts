import { Deletion } from 'skandha-facets';
import { DeleteBlogPostsResultT } from '/src/api/mutations/useDeleteBlogPosts';
import { BlogPostT } from '/src/api/types';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';

export type DeleteSelectionResultT = {
  result: DeleteBlogPostsResultT;
  isHighlightDeleted: boolean;
};

export class BlogPostsDeletion extends Deletion {
  constructor(private state: BlogPostsState) {
    super();
  }

  deleteSelection(): Promise<DeleteSelectionResultT> {
    const ctr = this.state.blogPostsCtr;
    // The selection only holds blog posts that exist
    const itemIds = ctr.selection.items.map((x: BlogPostT) => x.id);
    const isHighlightDeleted = itemIds.includes(ctr.highlight.itemId ?? '');
    return this.delete({ itemIds }).then((result: DeleteBlogPostsResultT) => ({
      result,
      isHighlightDeleted,
    }));
  }

  protected deleteItems(args: { itemIds: string[]; moveToTrash?: boolean }) {
    return this.state.props.deleteBlogPosts(args.itemIds).then((result) => {
      if (result.ok) {
        this.state.blogPostsCtr.selection.deselectItems({
          itemIds: args.itemIds,
        });
      }
      return result;
    });
  }
}
