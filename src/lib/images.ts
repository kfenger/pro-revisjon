import type { ImageMetadata } from 'astro';

// Optional images: drop a file into src/assets/images/ and it is picked up at build time.
// Missing files simply fall back (initials for staff, text wordmark for the logo).
const staff = import.meta.glob<{ default: ImageMetadata }>('../assets/images/ansatte/*.{jpg,jpeg,png,webp}', {
  eager: true,
});
const logos = import.meta.glob<{ default: ImageMetadata }>('../assets/images/logo.{png,jpg,jpeg,webp,svg}', {
  eager: true,
});
const photos = import.meta.glob<{ default: ImageMetadata }>('../assets/images/photos/*.{jpg,jpeg,png,webp}', {
  eager: true,
});

function find(map: Record<string, { default: ImageMetadata }>, base: string) {
  const key = Object.keys(map).find((k) => k.replace(/^.*\//, '').replace(/\.[^.]+$/, '') === base);
  return key ? map[key].default : undefined;
}

export const staffPhoto = (name: string) => find(staff, name);
export const logo = () => Object.values(logos)[0]?.default;
export const photo = (name: string) => find(photos, name);
