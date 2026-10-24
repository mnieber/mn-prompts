import type { Page, Route } from '@playwright/test';

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

export class FakeBackend {
  data: DataT = { userId: undefined, blogs: [], blogPosts: [] };
  requests: RequestT[] = [];
  unexpectedRequests: string[] = [];

  private failures: { [name: string]: ResponseT[] } = {};
  private idCounters: { [prefix: string]: number } = {};

  constructor(
    private apiUrl: string,
    private endpoints: EndpointT[]
  ) {}

  async install(page: Page) {
    await page.route(`${this.apiUrl}**`, (route) => this.handle(route));
  }

  /** Makes the next request to the endpoint fail with the given response. */
  failNext(name: string, response: ResponseT) {
    this.failures[name] = [...(this.failures[name] ?? []), response];
  }

  /** Returns a predictable id, e.g. `blog-1`. */
  nextId(prefix: string) {
    this.idCounters[prefix] = (this.idCounters[prefix] ?? 0) + 1;
    return `${prefix}-${this.idCounters[prefix]}`;
  }

  requestsOf(name: string) {
    return this.requests.filter((x) => x.name === name);
  }

  lastRequest(name: string): RequestT | undefined {
    return this.requestsOf(name).at(-1);
  }

  /**
   * Returns the response to a request. The url is either absolute or relative to the api url.
   * This is used by the page.route handler of the tests and by the playground server.
   */
  respond(method: string, url: string, body: any): ResponseT {
    const relativeUrl = url.startsWith(this.apiUrl)
      ? url.slice(this.apiUrl.length)
      : url;
    const path = '/' + relativeUrl.replace(/^\//, '').split('?')[0];

    for (const endpoint of this.endpoints) {
      const params = matchPath(endpoint.path, path);
      if (endpoint.method !== method || !params) continue;

      const fakeRequest = { name: endpoint.name, method, path, params, body };
      this.requests.push(fakeRequest);

      return (
        this.failures[endpoint.name]?.shift() ??
        endpoint.handle(this, fakeRequest)
      );
    }

    this.unexpectedRequests.push(`${method} ${path}`);
    return { status: 500, json: ['UNEXPECTED_REQUEST'] };
  }

  private async handle(route: Route) {
    const request = route.request();
    const body = request.postData() ? request.postDataJSON() : undefined;
    const response = this.respond(request.method(), request.url(), body);
    return route.fulfill({ status: response.status, json: response.json });
  }
}

function matchPath(pattern: string, path: string) {
  const names: string[] = [];
  const regex = pattern.replace(/:(\w+)/g, (_, name) => {
    names.push(name);
    return '([^/]+)';
  });
  const match = path.match(new RegExp(`^${regex}$`));
  if (!match) return undefined;
  return Object.fromEntries(
    names.map((name, i) => [name, decodeURIComponent(match[i + 1])])
  );
}
