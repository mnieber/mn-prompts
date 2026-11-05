import { Edit } from 'skandha-facets';
import { BlogsState } from '/src/blogs/BlogsState';

export class BlogsEdit extends Edit {
  constructor(private state: BlogsState) {
    super();
  }

  protected saveItem(args: { values: any }) {
    return this.state.props.saveBlog(args.values).then((result) => {
      if (result.ok) {
        this.state.blogsCtr.addition.confirm();
        this.reset();
      }
      return result;
    });
  }

  protected onCancel(): void {
    this.state.blogsCtr.addition.cancel();
  }
}
