import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://modelcoder.belownominal.com',
  output: 'static',
  server: {
    port: 4321,
    host: true
  }
});
