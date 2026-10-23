import { observer } from 'mobx-react-lite';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { BlogT, createBlog } from '/src/api/types/BlogT';
import { authStateCtx } from '/src/auth/hooks/useAuthStateContext';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { useRefUrl } from '/src/routes/hooks/useRefUrl';

type PropsT = {};

const ContextProps = {
  blogsAddition: blogsCtx.blogsAddition,
  authState: authStateCtx.authState,
};

export const CreateBlogEffect = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const { hasUrlChanged } = useRefUrl();
    const { blogsAddition } = props;

    React.useEffect(() => {
      if (hasUrlChanged) {
        if (!blogsAddition.item) {
          const values: BlogT = createBlog({});
          blogsAddition.add({ values });
        }
      }
    });

    return null;
  }, ContextProps)
);
