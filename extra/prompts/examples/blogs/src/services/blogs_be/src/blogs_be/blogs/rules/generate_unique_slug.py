from django.utils.text import slugify


def generate_unique_slug(text, fallback, taken_slugs):
    base_slug = slugify(text) or fallback

    slug = base_slug
    suffix = 2
    while slug in taken_slugs:
        slug = f"{base_slug}-{suffix}"
        suffix += 1

    return slug
