import * as Skandha from 'skandha';
import { Highlight } from 'skandha-facets';
import { CreateBlogPostResultT } from '/src/api/mutations/useCreateBlogPost';
import { DeleteBlogPostsResultT } from '/src/api/mutations/useDeleteBlogPosts';
import { MarkBlogPostAsPublishedResultT } from '/src/api/mutations/useMarkBlogPostAsPublished';
import { UpdateBlogPostResultT } from '/src/api/mutations/useUpdateBlogPost';
import { BlogPostT } from '/src/api/types';
import { BlogPostsAddition } from '/src/blogPosts/BlogPostsState/facets/BlogPostsAddition';
import { BlogPostsData } from '/src/blogPosts/BlogPostsState/facets/BlogPostsData';
import { BlogPostsDeletion } from '/src/blogPosts/BlogPostsState/facets/BlogPostsDeletion';
import { BlogPostsEdit } from '/src/blogPosts/BlogPostsState/facets/BlogPostsEdit';
import { BlogPostsSelection } from '/src/blogPosts/BlogPostsState/facets/BlogPostsSelection';
import { registerBlogPostsCtr } from '/src/blogPosts/BlogPostsState/registerBlogPostsCtr';
import { reformatBlogPost } from '/src/blogPosts/lib/reformatBlogPost';
import { bindActionsCtr } from '/src/utils/bindActionsCtr';
import { ObjT } from '/src/utils/types';

export type SaveBlogPostResultT = CreateBlogPostResultT | UpdateBlogPostResultT;

export type PropsT = {
  getBlogPosts: () => BlogPostT[];
  deleteBlogPosts: (ids: string[]) => Promise<DeleteBlogPostsResultT>;
  saveBlogPost: (values: ObjT) => Promise<SaveBlogPostResultT>;
  markBlogPostAsPublished: (
    blogPostId: string
  ) => Promise<MarkBlogPostAsPublishedResultT>;
};

export class BlogPostsState {
  props: PropsT;

  blogPostsCtr = {
    data: new BlogPostsData(),
    addition: new BlogPostsAddition(this),
    deletion: new BlogPostsDeletion(this),
    edit: new BlogPostsEdit(this),
    highlight: new Highlight<BlogPostT>(),
    selection: new BlogPostsSelection(this),
  };

  actionsCtr = {
    markBlogPostAsPublished: (blogPostId: string) => {
      return this.props.markBlogPostAsPublished(blogPostId);
    },
    reformatBlogPost: (blogPostId: string) => {
      return reformatBlogPost(this.blogPostsCtr.data.blogPostById[blogPostId]);
    },
  };

  destroy() {
    Skandha.cleanUpCtr(this);
  }

  constructor(props: PropsT) {
    this.props = props;
    bindActionsCtr(this.actionsCtr, this);
    registerBlogPostsCtr(this);
  }
}
