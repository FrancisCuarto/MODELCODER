import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: process.env.SITE_URL || 'https://modelcoder.vercel.app',
  output: 'static',
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.8,
      lastmod: new Date()
    })
  ],
  server: {
    port: 4321,
    host: true
  }
});
