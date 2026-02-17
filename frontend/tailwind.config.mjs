/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,vue}'],
  theme: {
    extend: {
      colors: {
        dark: { 900: '#080810', 800: '#0D0D18', 700: '#12121F', 600: '#1A1A38', 500: '#2A2A58' },
        neon: { blue: '#00D4FF', purple: '#9B5CFF', pink: '#FF2D9B', green: '#00FF88' },
      },
      fontFamily: {
        display: ['Outfit', 'sans-serif'],
        body: ['DM Sans', 'sans-serif'],
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'slide-up': 'slideUp 0.5s cubic-bezier(0.16,1,0.3,1)',
        'fade-in': 'fadeIn 0.4s ease-out',
        'gradient': 'gradient 8s ease infinite',
        'bounce-in': 'bounceIn 0.6s cubic-bezier(0.16,1,0.3,1)',
        'spin-slow': 'spin 20s linear infinite',
      },
      keyframes: {
        float: { '0%,100%': { transform: 'translateY(0px)' }, '50%': { transform: 'translateY(-20px)' } },
        slideUp: { '0%': { transform: 'translateY(30px)', opacity: '0' }, '100%': { transform: 'translateY(0)', opacity: '1' } },
        fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
        gradient: { '0%,100%': { backgroundPosition: '0% 50%' }, '50%': { backgroundPosition: '100% 50%' } },
        bounceIn: { '0%': { transform: 'scale(0.8)', opacity: '0' }, '60%': { transform: 'scale(1.05)' }, '100%': { transform: 'scale(1)', opacity: '1' } },
      },
    },
  },
  plugins: [],
}
