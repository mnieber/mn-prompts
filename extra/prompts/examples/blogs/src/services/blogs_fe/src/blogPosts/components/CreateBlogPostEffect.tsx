import { observer } from 'mobx-react-lite';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { BlogPostT, createBlogPost } from '/src/api/types/BlogPostT';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { useRefUrl } from '/src/routes/hooks/useRefUrl';

type PropsT = {};

const ContextProps = {
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
};

export const CreateBlogPostEffect = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const { hasUrlChanged } = useRefUrl();
    const { blogPostsAddition } = props;

    React.useEffect(() => {
      // If there is a new url
      if (hasUrlChanged) {
        if (!blogPostsAddition.item) {
          const values: BlogPostT = createBlogPost({});
          blogPostsAddition.add({ values });
        }
      }
    });

    return null;
  }, ContextProps)
);
