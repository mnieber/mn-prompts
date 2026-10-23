import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '/src/api/queryClient';
import { AuthStateProvider } from '/src/auth/components/AuthStateProvider';

export type PropsT = React.PropsWithChildren<{}>;

export const StorybookProvider = (props: PropsT) => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthStateProvider>{props.children}</AuthStateProvider>
    </QueryClientProvider>
  );
};
