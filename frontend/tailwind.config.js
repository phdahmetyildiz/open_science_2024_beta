// This file is being archived on 15.11.2026 and is not part of the new version.
/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addUtilities, addComponents, e, config }) {
      // Add your custom styles here
    }),
  ]
}
module.exports = {
  daisyui: {
    themes: ["light", "dark", "autumn", "nord"],
  },
  content: [
    "./templates/**/*.{html,js}",
    "./templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
}

