import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "e2e",
  timeout: 60000,
  use: {
    baseURL: process.env.AML_URL ?? "http://localhost:8080",
    headless: true,
    trace: "off",
    screenshot: "only-on-failure",
  },
  workers: 1,
});
