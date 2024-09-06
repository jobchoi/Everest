// tailwind.config.js
const { createGlobPatternsForDependencies } = require('@nx/angular/tailwind');
const { join } = require('path');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    join(__dirname, 'src/**/!(*.stories|*.spec).{ts,html}'),
    ...createGlobPatternsForDependencies(__dirname),
  ],
  theme: {
    extend: {
      colors: {
        uFFEDDC: '#FFEDDC',
      },
      lineHeight: {
        'u19.97': '19.97px',
      },
    },
  },
  plugins: [],
};
