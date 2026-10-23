import { history } from '/src/routes/history';
import { navHandler, RouteSpecT } from '/src/routes/navHandler';
import { generatePath } from '/src/routes/utils/generatePath';

export const blogPostsRoutes = {
  blogPost: () => '/blogs/:blogSlug/blog-posts/:blogPostSlug',
  createBlogPost: () => '/blogs/:blogSlug/blog-posts/create/_',
};

export class BlogPostsNav {
  blogPost(
    params: { blogSlug: string; blogPostSlug: string },
    callerId?: string
  ): RouteSpecT {
    return navHandler().run('blogPost', params, callerId);
  }
  createBlogPost(params: { blogSlug: string }, callerId?: string): RouteSpecT {
    return navHandler().run('createBlogPost', params, callerId);
  }
}

export class DefaultBlogPostsNavHandler extends BlogPostsNav {
  blogPost(
    params: { blogSlug: string; blogPostSlug: string },
    callerId?: string
  ) {
    return {
      url: generatePath(blogPostsRoutes.blogPost(), params),
      nav: history.push,
    };
  }

  createBlogPost(params: { blogSlug: string }, callerId?: string) {
    return {
      url: generatePath(blogPostsRoutes.createBlogPost(), params),
      nav: history.push,
    };
  }
}

export const blogPostsNav = new BlogPostsNav();
