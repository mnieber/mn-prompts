import { Edit } from 'skandha-facets';
import { BlogsState } from '/src/blogs/BlogsState';
import { ObjT } from '/src/utils/types';

export class BlogsEdit extends Edit {
  constructor(private state: BlogsState) {
    super();
  }

  protected saveItem(args: { values: any }): any {
    return this.state.props.saveBlog(args.values).then((response: ObjT) => {
      this.state.blogsCtr.addition.confirm();
      return response;
    });
  }

  protected onCancel(): void {
    this.state.blogsCtr.addition.cancel();
  }
}
