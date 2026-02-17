/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Paleta estilo Apple
        apple: {
          blue: '#0071E3',
          lightblue: '#2997FF',
          green: '#34C759',
          red: '#FF3B30',
          orange: '#FF9500',
          gray: {
            50: '#FAFAFA',
            100: '#F5F5F7',
            200: '#E8E8ED',
            300: '#D2D2D7',
            400: '#AEAEB2',
            500: '#86868B',
            600: '#6E6E73',
            700: '#515154',
            800: '#3A3A3C',
            900: '#1D1D1F',
          }
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'SF Pro Display', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      borderRadius: {
        '2xl': '1.25rem',
        '3xl': '1.5rem',
      },
      boxShadow: {
        'apple': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'apple-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
