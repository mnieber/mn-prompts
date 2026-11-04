import { Edit } from 'skandha-facets';
import { isFailedMutation } from '/src/api/utils/isFailedMutation';
import { BlogsState } from '/src/blogs/BlogsState';
import { ObjT } from '/src/utils/types';

export class BlogsEdit extends Edit {
  constructor(private state: BlogsState) {
    super();
  }

  protected saveItem(args: { values: any }): any {
    return this.state.props.saveBlog(args.values).then((response: ObjT) => {
      if (isFailedMutation(response)) {
        // Rejecting keeps the form in edit mode, because Edit.save skips its reset
        this.setIsSaving(false);
        throw response;
      }
      this.state.blogsCtr.addition.confirm();
      return response;
    });
  }

  protected onCancel(): void {
    this.state.blogsCtr.addition.cancel();
  }
}
