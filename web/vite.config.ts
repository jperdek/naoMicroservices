import path from "path";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { nodePolyfills } from 'vite-plugin-node-polyfills';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), nodePolyfills({
      include: ['crypto', 'stream', 'buffer'],
    })],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      // Upload + run → translatorapi
      "/exercise/from_video": {
        target: "http://localhost:7000",
        changeOrigin: true,
      },
      // run endpoint: /exercise/<id>/run
      "^/exercise/[^/]+/run$": {
        target: "http://localhost:7000",
        changeOrigin: true,
      },
      // frames, sequence, images → exerciseconfigservice
      "/exercise": {
        target: "http://localhost:7001",
        changeOrigin: true,
      },
      // voice command / pose registry
      "/commands": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  }
});
