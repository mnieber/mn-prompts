import { observer } from 'mobx-react-lite';
import * as R from 'ramda';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { useParams } from 'wouter';
import { BlogPostT } from '/src/api/types/BlogPostT';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { useRefUrl } from '/src/routes/hooks/useRefUrl';
import { UrlEffectView } from '/src/utils/components';
import { ObjT } from '/src/utils/types';

type PropsT = {};

const ContextProps = {
  blog: blogsCtx.blog,
  blogPost: blogPostsCtx.blogPost,
  blogPosts: blogPostsCtx.blogPosts,
  blogPostsSelection: blogPostsCtx.blogPostsSelection,
};

export const SelectBlogPostEffect = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const params = useParams() as ObjT;
    const { updateRefUrl, hasUrlChanged } = useRefUrl();

    const { blogPostsSelection, blogPost, blogPosts } = props;
    const blogPostFromUrl = R.find(
      (x: BlogPostT) => x.slug === params.blogPostSlug
    )(blogPosts);
    const isBlogPostInSyncWithUrl = blogPost?.id === blogPostFromUrl?.id;

    const selectBlogPost = (blogPost?: BlogPostT) => {
      blogPostsSelection.selectItem({ itemId: blogPost?.id });
    };

    React.useEffect(() => {
      // If there is a new url
      if (hasUrlChanged) {
        if (blogPostFromUrl) {
          updateRefUrl();
          if (!isBlogPostInSyncWithUrl) {
            selectBlogPost(blogPostFromUrl);
          }
        } else {
          selectBlogPost(undefined);
        }
      }
    });

    return (
      <UrlEffectView
        resourceName="blog-post"
        isInSync={isBlogPostInSyncWithUrl}
        className="absolute"
      />
    );
  }, ContextProps)
);
