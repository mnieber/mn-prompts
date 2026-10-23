import { observer } from 'mobx-react-lite';
import { withContextProps } from 'react-props-from-context';
import { Route, Switch } from 'wouter';
import { BlogsPage } from '/src/blogs/components';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { blogsNav } from '/src/blogs/routes';
import { framesRoutes } from '/src/frames/routes';
import { RedirectEffect } from '/src/routes/components/RedirectEffect';
import { ext } from '/src/routes/navHandler';

type PropsT = {};

const ContextProps = {
  blogsHighlight: blogsCtx.blogsHighlight,
};

export const BlogsSwitch = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    return (
      <Switch>
        <Route path={ext(framesRoutes.dashboard())}>
          <BlogsPage className="grow" />
          <Route path={framesRoutes.dashboard()}>
            <RedirectEffect
              getRoute={() => {
                if (props.blogsHighlight.item) {
                  return blogsNav.blog({
                    blogSlug: props.blogsHighlight.item.slug,
                  });
                }
                return undefined;
              }}
            />
          </Route>
        </Route>
      </Switch>
    );
  }, ContextProps)
);
