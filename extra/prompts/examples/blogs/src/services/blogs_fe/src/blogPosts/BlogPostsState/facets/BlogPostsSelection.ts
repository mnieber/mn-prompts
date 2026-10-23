import { Selection, handleSelectItem } from 'skandha-facets';
import { BlogPostT } from '/src/api/types';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';

export class BlogPostsSelection extends Selection<BlogPostT> {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected performSelection(args: { itemId: string; isCtrl: boolean; isShift: boolean }): void {
    handleSelectItem(this, args);
    if (!args.isCtrl && !args.isShift) {
      this.state.blogPostsCtr.highlight.set({ itemId: args.itemId });
    }
  }
}
