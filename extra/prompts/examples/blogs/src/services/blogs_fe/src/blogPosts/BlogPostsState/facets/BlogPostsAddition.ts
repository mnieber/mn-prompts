import { Addition } from 'skandha-facets';
import { BlogPostT } from '/src/api/types';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';

export class BlogPostsAddition extends Addition<BlogPostT> {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected stageAdd(): void {
    this.parentId = this.state.blogPostsCtr.highlight.itemId;
  }

  protected highlightNewItem(item: BlogPostT): void {
    this.state.blogPostsCtr.selection.selectItem({ itemId: item.id });
    this.state.blogPostsCtr.edit.enable();
  }

  protected unstageAdd(parentId: string | undefined): void {
    this.state.blogPostsCtr.edit.cancel();
  }
}
