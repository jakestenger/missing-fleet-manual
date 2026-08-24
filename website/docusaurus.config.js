// @ts-check
/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'The Missing Fleet Manual',
  tagline: 'How Fleet is built, and what it is for',
  favicon: 'img/favicon.ico',
  url: process.env.SITE_URL || 'http://localhost',
  baseUrl: '/',

  // Forward links to unwritten sections are deliberate claims on future filenames
  // (see OUTLINE.md "Filename registry"). Warn, do not fail the build.
  onBrokenLinks: 'warn',
  themes: ['@docusaurus/theme-mermaid'],

  markdown: {
    format: 'md',
    mermaid: true,
    hooks: { onBrokenMarkdownLinks: 'warn', onBrokenMarkdownImages: 'warn' },
  },

  presets: [
    ['classic', {
      docs: {
        // Source of truth stays in the Obsidian vault. The site reads it in place.
        path: '../manual',
        routeBasePath: '/',
        sidebarPath: './sidebars.js',
        include: ['**/*.md'],
        exclude: ['**/_*.md'],
      },
      blog: false,
      theme: { customCss: './src/css/custom.css' },
    }],
  ],

  themeConfig: {
    navbar: {
      title: 'The Missing Fleet Manual',
      items: [{ type: 'docSidebar', sidebarId: 'manualSidebar', position: 'left', label: 'Contents' }],
    },
    docs: { sidebar: { hideable: true, autoCollapseCategories: false } },
    colorMode: { defaultMode: 'light', respectPrefersColorScheme: true },
    prism: { additionalLanguages: ['sql', 'bash', 'json', 'yaml', 'go', 'powershell'] },
  },
};
module.exports = config;
