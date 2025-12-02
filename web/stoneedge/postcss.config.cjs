module.exports = {
  plugins: {
    'postcss-import': {},
    'postcss-nested': {},
    '@tailwindcss/postcss': {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {})
  }
}