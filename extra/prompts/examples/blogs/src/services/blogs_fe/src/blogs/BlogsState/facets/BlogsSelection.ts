import { Selection, handleSelectItem } from 'skandha-facets';
import { BlogT } from '/src/api/types';
import { BlogsState } from '/src/blogs/BlogsState';

export class BlogsSelection extends Selection<BlogT> {
  constructor(private state: BlogsState) {
    super();
  }

  protected performSelection(args: { itemId: string; isCtrl: boolean; isShift: boolean }): void {
    handleSelectItem(this, args);
    if (!args.isCtrl && !args.isShift) {
      this.state.blogsCtr.highlight.set({ itemId: args.itemId });
    }
  }
}
