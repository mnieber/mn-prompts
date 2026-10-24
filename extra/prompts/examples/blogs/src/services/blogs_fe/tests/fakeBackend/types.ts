import type { FakeBackend } from '/tests/fakeBackend/FakeBackend';

export type BlogRowT = {
  id: string;
  name: string;
  slug: string;
  description: string;
};

export type BlogPostRowT = {
  id: string;
  blog_id: string;
  title: string;
  slug: string;
  content: string;
  is_published: boolean;
  level: 'easy' | 'medium' | 'hard';
};

export type DataT = {
  userId: string | undefined;
  blogs: BlogRowT[];
  blogPosts: BlogPostRowT[];
  blogTags: string[];
};

export type RequestT = {
  name: string;
  method: string;
  path: string;
  params: Record<string, string>;
  body: any;
};

export type ResponseT = {
  status: number;
  json: any;
};

export type EndpointT = {
  // The name of the query or mutation hook (e.g. `createBlog` for `useCreateBlog`)
  name: string;
  method: 'GET' | 'POST';
  // A path relative to the api url, with `:param` tokens
  path: string;
  handle: (backend: FakeBackend, request: RequestT) => ResponseT;
};
