import { Addition, topOfTheList } from 'skandha-facets';
import { BlogT } from '/src/api/types';
import { BlogsState } from '/src/blogs/BlogsState';

export class BlogsAddition extends Addition<BlogT> {
  constructor(private state: BlogsState) {
    super();
  }

  protected stageAdd(): void {
    this.parentId = topOfTheList;
  }

  protected unstageAdd(parentId: string | undefined): void {
    this.state.blogsCtr.edit.cancel();
  }
}
