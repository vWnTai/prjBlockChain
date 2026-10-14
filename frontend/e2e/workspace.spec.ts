import { test, expect } from "@playwright/test";
import { readFileSync, mkdirSync } from "node:fs";
const env = Object.fromEntries(
  readFileSync(new URL("../../.env", import.meta.url), "utf8")
    .split(/\r?\n/)
    .filter((l) => l && !l.startsWith("#"))
    .map((l) => l.split("=")),
);
test("local dashboard, evidence review, timeline and mobile layout", async ({
  page,
}) => {
  const errors: string[] = [];
  await page.setViewportSize({ width: 1440, height: 1000 });
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await page.getByLabel("Tên đăng nhập").fill("admin");
  await page.getByLabel("Mật khẩu", { exact: true }).fill(env.ADMIN_PASSWORD);
  await page.getByRole("button", { name: "Vào workspace" }).click();
  await expect(
    page.getByRole("heading", { name: "Điều khiển mô phỏng", exact: true }),
  ).toBeVisible();
  await expect(page.locator("#run-picker")).not.toHaveValue("");
  await expect(
    page.getByText("Hoàn thành", { exact: true }).first(),
  ).toBeVisible({ timeout: 30000 });
  await expect(page.locator(".graph-legend small").first()).toContainText(
    /[1-9]\d* nodes/,
  );
  await expect(page.locator(".graph-canvas canvas").first()).toBeVisible();
  mkdirSync(new URL("../../artifacts/", import.meta.url), { recursive: true });
  await page.screenshot({
    path: "../artifacts/dashboard-desktop.png",
    fullPage: false,
  });
  await page.getByRole("button", { name: "Cảnh báo & đánh giá" }).click();
  await expect(
    page.getByRole("heading", { name: "Hàng đợi xem xét" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Xem bằng chứng" }).first().click();
  await expect(
    page.getByRole("heading", { name: /Bằng chứng:/ }),
  ).toBeVisible();
  await expect(page.locator(".evidence-list button").first()).toBeVisible();
  await expect(page.locator(".graph-loading")).toHaveCount(0);
  await expect(page.locator(".explorer-toolbar .subtle-tag")).toContainText(
    /[1-9]\d* NODES/,
  );
  const size = await page.locator(".graph-canvas canvas").first().boundingBox();
  expect(size?.height).toBeGreaterThan(300);
  await page.screenshot({
    path: "../artifacts/evidence-desktop.png",
    fullPage: false,
  });
  await page
    .getByLabel("Nhận xét analyst")
    .fill("E2E: inspected causal evidence");
  await page.getByRole("button", { name: "Lưu đánh giá" }).click();
  await expect(page.getByText("E2E: inspected causal evidence")).toBeVisible();
  const slider = page.locator("#timeline");
  await slider.focus();
  await page.keyboard.press("Home");
  await page.keyboard.press("ArrowRight");
  await expect(slider).toHaveValue("1");
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(
    page.getByRole("heading", { name: "Khám phá dòng tiền", exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBeTruthy();
  await page.screenshot({
    path: "../artifacts/dashboard-mobile.png",
    fullPage: true,
  });
  expect(errors).toEqual([]);
});
