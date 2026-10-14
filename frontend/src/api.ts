let csrfToken = "";
export function query(
  params: Record<string, string | number | undefined>,
): string {
  return new URLSearchParams(
    Object.entries(params)
      .filter(
        (entry): entry is [string, string | number] => entry[1] !== undefined,
      )
      .map(([k, v]) => [k, String(v)]),
  ).toString();
}
export async function api<T>(
  path: string,
  method = "GET",
  body?: unknown,
  signal?: AbortSignal,
  headers: Record<string, string> = {},
): Promise<T> {
  const response = await fetch("/api" + path, {
    method,
    signal,
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-Token": csrfToken,
      ...headers,
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const result = await response.json();
  if (!response.ok)
    throw new Error(
      typeof result.message === "string"
        ? result.message
        : typeof result.detail === "string"
          ? result.detail
          : JSON.stringify(result.detail ?? result),
    );
  if (result.csrf_token) csrfToken = result.csrf_token;
  return result as T;
}
