export function formatMoney(base: string, decimals = 6): string {
  if (
    !/^-?\d+$/.test(base) ||
    !Number.isInteger(decimals) ||
    decimals < 0 ||
    decimals > 18
  )
    throw new Error("Invalid integer money");
  const negative = base.startsWith("-");
  const value = BigInt(base.startsWith("-") ? base.slice(1) : base);
  const unit = 10n ** BigInt(decimals);
  const fraction = (value % unit)
    .toString()
    .padStart(decimals, "0")
    .replace(/0+$/, "");
  return (
    (negative ? "-" : "") +
    (value / unit).toLocaleString("vi-VN") +
    (fraction ? "," + fraction : "")
  );
}
export function parseSIM(value: string): string {
  if (!/^\d+(?:[.,]\d{1,6})?$/.test(value))
    throw new Error("SIM requires at most 6 decimal digits");
  const [whole, fraction = ""] = value.replace(",", ".").split(".");
  return (
    BigInt(whole) * 1000000n +
    BigInt(fraction.padEnd(6, "0"))
  ).toString();
}
