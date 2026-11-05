/** The rule of the real backend for the slug of a new blog or blog post. */
export const generateUniqueSlug = (
  text: string,
  fallback: string,
  takenSlugs: string[]
) => {
  const baseSlug =
    text
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .trim()
      .replace(/[\s-]+/g, '-') || fallback;

  let slug = baseSlug;
  for (let suffix = 2; takenSlugs.includes(slug); suffix++) {
    slug = `${baseSlug}-${suffix}`;
  }
  return slug;
};
