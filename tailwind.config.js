/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
  "./manager/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [
  require('@tailwindcss/forms')],
}

