/** @type {import('tailwindcss').Config} */
module.exports = {
  important: true,
  content: [

    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/src/**/*.js',

  ],
  theme: {
    extend: {
      colors: {
        hop: "#5B8C3A",
        offwhite: "#F8F5F0",
        malt: "#D4A017",
        purple: "#6A4C93",
        warmgray: "#D3CEC4",
      },
    },
  },
  plugins: [],
};
