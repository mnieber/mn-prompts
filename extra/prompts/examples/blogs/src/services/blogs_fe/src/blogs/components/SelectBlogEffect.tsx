import { observer } from 'mobx-react-lite';
import * as R from 'ramda';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { useParams } from 'wouter';
import { BlogT } from '/src/api/types/BlogT';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { useRefUrl } from '/src/routes/hooks/useRefUrl';
import { UrlEffectView } from '/src/utils/components';
import { ObjT } from '/src/utils/types';

type PropsT = {};

const ContextProps = {
  blogs: blogsCtx.blogs,
  blog: blogsCtx.blog,
  blogsSelection: blogsCtx.blogsSelection,
};

export const SelectBlogEffect = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const params = useParams() as ObjT;
    const { updateRefUrl, hasUrlChanged } = useRefUrl();

    const { blogsSelection, blog, blogs } = props;
    const blogFromUrl = R.find((x: BlogT) => x.slug === params.blogSlug)(blogs);
    const isBlogInSyncWithUrl = blog?.id === blogFromUrl?.id;

    const selectBlog = (blog?: BlogT) => {
      blogsSelection.selectItem({ itemId: blog?.id });
    };

    React.useEffect(() => {
      // If there is a new url
      if (hasUrlChanged) {
        if (blogFromUrl) {
          updateRefUrl();
          if (!isBlogInSyncWithUrl) {
            selectBlog(blogFromUrl);
          }
        } else {
          selectBlog(undefined);
        }
      }
    });

    return (
      <UrlEffectView
        resourceName="blog"
        isInSync={isBlogInSyncWithUrl}
        className="absolute"
      />
    );
  }, ContextProps)
);
