import { Meta, StoryObj } from '@storybook/react';
import { StorybookProvider } from '/src/app/components';
import { BlogListView } from '/src/blogs/components';
import { BlogsStateProvider } from '/src/blogs/components/BlogsStateProvider';
import { passthroughHandlers } from '/src/mocks/browser/defaultPassthrough';
import { handleGetBlogs } from '/src/mocks/queries/handleGetBlogs';

const meta: Meta<typeof BlogListView> = {
  component: BlogListView,
  parameters: {
    msw: {
      handlers: [handleGetBlogs, ...passthroughHandlers],
    },
  },
};

export default meta;

type Story = StoryObj<typeof BlogListView>;

export const Default: Story = {
  render: () => {
    return (
      <StorybookProvider>
        <BlogsStateProvider>
          <BlogListView />
        </BlogsStateProvider>
      </StorybookProvider>
    );
  },
};
