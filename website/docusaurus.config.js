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
        // Versioned per Fleet MINOR line (STYLE.md, "Point releases are footnotes").
        // The living docs in ../manual are the newest minor being worked; released
        // minors are frozen under versioned_docs/ and picked from the navbar dropdown.
        // Bumping a minor: freeze the outgoing line with `docusaurus docs:version <minor>`,
        // then relabel current below to the new minor.
        lastVersion: 'current',
        versions: {
          current: { label: '4.91', path: '' },
        },
      },
      blog: false,
      theme: { customCss: './src/css/custom.css' },
    }],
  ],

  themeConfig: {
    navbar: {
      title: 'The Missing Fleet Manual',
      items: [
        { type: 'docSidebar', sidebarId: 'manualSidebar', position: 'left', label: 'Contents' },
        { type: 'docsVersionDropdown', position: 'right' },
      ],
    },
    docs: { sidebar: { hideable: true, autoCollapseCategories: false } },
    colorMode: { defaultMode: 'light', respectPrefersColorScheme: true },
    prism: { additionalLanguages: ['sql', 'bash', 'json', 'yaml', 'go', 'powershell'] },
  },
};
module.exports = config;
