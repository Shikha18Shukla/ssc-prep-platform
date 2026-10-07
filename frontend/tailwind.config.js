/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#F8F9FA",
        card: "#FFFFFF",
        content: "#2D3436",
        primary: {
          DEFAULT: "#007BFF",
          50: "#E6F0FF",
          100: "#CCE0FF",
          200: "#99C2FF",
          300: "#66A3FF",
          400: "#3385FF",
          500: "#007BFF",
          600: "#0062CC",
          700: "#004A99",
          800: "#003166",
          900: "#001933",
        },
        accent: {
          DEFAULT: "#FF6B35",
          50: "#FFF0EB",
          100: "#FFE1D6",
          200: "#FFC3AD",
          300: "#FFA585",
          400: "#FF885C",
          500: "#FF6B35",
          600: "#CC5529",
          700: "#99401F",
          800: "#662B14",
          900: "#33150A",
        },
        correct: "#28C76F",
        wrong: "#EA5455",
      },
      fontFamily: {
        sans: ["Inter", "Noto Sans Devanagari", "system-ui", "sans-serif"],
        devanagari: ["Noto Sans Devanagari", "sans-serif"],
      },
      maxWidth: {
        card: "700px",
      },
      fontSize: {
        question: ["1.25rem", { lineHeight: "1.7" }],
        option: ["1.125rem", { lineHeight: "1.7" }],
      },
    },
  },
  plugins: [],
};
