// app/api/ping-ollama/route.ts
export const runtime = "nodejs";

export async function GET() {
  const r = await fetch("http://127.0.0.1:11434/v1/models");
  const j = await r.json();
  return new Response(JSON.stringify(j, null, 2), { headers: { "content-type": "application/json" } });
}
