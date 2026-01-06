module.exports = {
  darkMode: ['class'],
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#050505',
        surface: '#0F0F0F',
        'surface-highlight': '#1A1A1A',
        primary: '#D4AF37',
        'primary-muted': '#8A7020',
        'text-main': '#F2F2F2',
        'text-muted': '#A1A1A1',
        border: '#262626',
        error: '#7F1D1D',
        success: '#14532D',
      },
      fontFamily: {
        serif: ['Playfair Display', 'serif'],
        sans: ['Manrope', 'sans-serif'],
      },
      borderRadius: {
        none: '0',
        sm: '2px',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};