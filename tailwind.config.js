module.exports = {
  content: ["./app/templates/**/*.html", "./app/static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        'lagon-blue': '#00B4D8',
        'lagon-navy': '#023E8A',
        'lagon-coral': '#FF6B6B',
        'lagon-light': '#F8F9FA',
        'lagon-dark': '#2B2D42',
      },
      fontFamily: {
        'sans': ['Inter', 'ui-sans-serif', 'system-ui'],
        'serif': ['Playfair Display', 'ui-serif', 'Georgia'],
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ]
}
