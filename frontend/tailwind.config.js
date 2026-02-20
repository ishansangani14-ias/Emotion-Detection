/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#FF6B35',
          dark: '#E55A2A',
          light: '#FF8C5A',
        },
        bg: {
          primary: '#0F0F0F',
          secondary: '#1A1A1A',
          tertiary: '#252525',
        },
        text: {
          primary: '#FFFFFF',
          secondary: '#E0E0E0',
          tertiary: '#999999',
        },
        border: {
          primary: '#3A3A3A',
          secondary: '#2A2A2A',
        },
        success: '#4CAF50',
        error: '#F44336',
        warning: '#FFC107',
        info: '#2196F3',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      keyframes: {
        bounce: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        fall: {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(10px)' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-10px)' },
          '75%': { transform: 'translateX(10px)' },
        },
        pop: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.3)' },
          '100%': { transform: 'scale(1)' },
        },
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        fade: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        distort: {
          '0%, 100%': { transform: 'rotate(0deg) scale(1)' },
          '25%': { transform: 'rotate(-5deg) scale(0.95)' },
          '75%': { transform: 'rotate(5deg) scale(1.05)' },
        },
      },
      animation: {
        bounce: 'bounce 1s ease-in-out infinite',
        fall: 'fall 2s ease-in-out infinite',
        shake: 'shake 0.5s ease-in-out infinite',
        pop: 'pop 0.6s ease-in-out infinite',
        pulse: 'pulse 2s ease-in-out infinite',
        fade: 'fade 3s ease-in-out infinite',
        distort: 'distort 1s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
