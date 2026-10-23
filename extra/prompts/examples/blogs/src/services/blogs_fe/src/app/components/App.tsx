import { QueryClientProvider } from '@tanstack/react-query';
import * as R from 'ramda';
import { queryClient } from '/src/api/queryClient';
import { flags } from '/src/app/flags';
import { AuthStateProvider } from '/src/auth/components/AuthStateProvider';
import { AuthSwitch } from '/src/auth/components/AuthSwitch';
import { BlogPostsStateProvider } from '/src/blogPosts/components/BlogPostsStateProvider';
import { BlogsStateProvider } from '/src/blogs/components/BlogsStateProvider';
import { BlogsSwitch } from '/src/blogs/components/BlogsSwitch';
import { DashboardFrame } from '/src/frames/components/DashboardFrame';
import { MainView } from '/src/frames/components/MainView';
import { L } from '/src/frames/layout';
import { MockApp } from '/src/mocks/app/components/MockApp';
import { NavStateProvider } from '/src/routes/components/NavStateProvider';
import { cn } from '/src/utils/classnames';

export const App = () => {
  return flags.mockApp ? (
    <AppBody>
      <MockApp />
    </AppBody>
  ) : (
    <QueryClientProvider client={queryClient}>
      <AuthStateProvider>
        <NavStateProvider>
          <AppBody>
            <DashboardFrame>
              <AuthSwitch />
              <BlogsStateProvider>
                <BlogPostsStateProvider>
                  <MainView className="">
                    <BlogsSwitch />
                  </MainView>
                </BlogPostsStateProvider>
              </BlogsStateProvider>
            </DashboardFrame>
          </AppBody>
        </NavStateProvider>
      </AuthStateProvider>
    </QueryClientProvider>
  );
};

const AppBody = (props: React.PropsWithChildren<{}>) => {
  return (
    <div
      id="App"
      className={cn('App', [
        R.values({
          root: L.col.banner(),
          // 320px = breakpoints.xs
          size: `min-width-[320px] h-screen max-w-[1600px]`,
          pos: `mx-auto`,
          scroll: 'overflow-x-hidden',
        }),
      ])}
      tabIndex={0}
      ref={(x: any) => x?.focus()}
    >
      {props.children}
    </div>
  );
};
