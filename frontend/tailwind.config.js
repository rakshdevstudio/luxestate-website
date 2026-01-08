module.exports = {
  darkMode: ['class'],
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#030303', // Richer, deeper black
        surface: '#0A0A0A',
        'surface-highlight': '#141414',
        primary: '#D4AF37', // Classic Gold
        'primary-light': '#F2C94C', // Brighter Gold for gradients/hover
        'primary-dark': '#8A7020', // Darker Gold for depth
        'primary-muted': '#6B5B2E',
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
        md: '4px',
        lg: '8px',
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.8s ease-out forwards',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '200% 0' },
          '100%': { backgroundPosition: '-200% 0' },
        },
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};