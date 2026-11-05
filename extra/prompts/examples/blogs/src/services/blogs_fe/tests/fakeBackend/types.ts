import type { FakeBackend } from '/tests/fakeBackend/FakeBackend';

export type BlogRowT = {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  owner_id: string;
};

export type BlogPostRowT = {
  id: string;
  blog_id: string;
  title: string;
  slug: string;
  content: string | null;
  is_published: boolean;
  level: 'easy' | 'medium' | 'hard';
};

export type DataT = {
  userId: string | undefined;
  blogs: BlogRowT[];
  blogPosts: BlogPostRowT[];
};

export type RequestT = {
  name: string;
  method: string;
  path: string;
  params: Record<string, string>;
  body: any;
  headers: Record<string, string>;
};

export type ResponseT = {
  status: number;
  json?: any;
};

export type EndpointT = {
  // The name of the query or mutation hook (e.g. `createBlog` for `useCreateBlog`)
  name: string;
  method: 'GET' | 'POST' | 'DELETE';
  // A path relative to the api url, with `:param` tokens
  path: string;
  handle: (backend: FakeBackend, request: RequestT) => ResponseT;
};
