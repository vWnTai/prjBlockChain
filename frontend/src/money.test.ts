import { describe, it, expect } from "vitest";
import { formatMoney, parseSIM } from "./money";
describe("exact SIM units", () => {
  it("preserves values larger than 2^53", () =>
    expect(parseSIM("9007199254.740993")).toBe("9007199254740993"));
  it("renders all six fractional units", () =>
    expect(formatMoney("9007199254740993")).toBe("9.007.199.254,740993"));
  it("preserves T boundaries", () => {
    expect(formatMoney("999999999")).toBe("999,999999");
    expect(formatMoney("1000000000")).toBe("1.000");
    expect(formatMoney("1000000001")).toBe("1.000,000001");
  });
  it("rejects fractional base units and excessive precision", () => {
    expect(() => formatMoney("1.2")).toThrow();
    expect(() => parseSIM("1.0000001")).toThrow();
    expect(() => parseSIM("1e3")).toThrow();
  });
});
