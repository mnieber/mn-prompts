import { DefaultAuthNavHandler } from '/src/auth/routes';
import { DefaultBlogPostsNavHandler } from '/src/blogPosts/routes';
import { DefaultBlogsNavHandler } from '/src/blogs/routes';
import { NavHandler } from '/src/routes/navHandler';

export const createNavHandler = () => {
  const navHandler = new NavHandler();
  navHandler.installDefaultNavHandler(new DefaultBlogsNavHandler());
  navHandler.installDefaultNavHandler(new DefaultBlogPostsNavHandler());
  navHandler.installDefaultNavHandler(new DefaultAuthNavHandler());
  return navHandler;
};
