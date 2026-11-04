import { Edit } from 'skandha-facets';
import { isFailedMutation } from '/src/api/utils/isFailedMutation';
import { BlogPostsState } from '/src/blogPosts/BlogPostsState';
import { ObjT } from '/src/utils/types';

export class BlogPostsEdit extends Edit {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected saveItem(args: { values: any }): any {
    return this.state.props.saveBlogPost(args.values).then((response: ObjT) => {
      if (isFailedMutation(response)) {
        // Rejecting keeps the form in edit mode, because Edit.save skips its reset
        this.setIsSaving(false);
        throw response;
      }
      this.state.blogPostsCtr.addition.confirm();
      return response;
    });
  }

  protected onCancel(): void {
    this.state.blogPostsCtr.addition.cancel();
  }
}
