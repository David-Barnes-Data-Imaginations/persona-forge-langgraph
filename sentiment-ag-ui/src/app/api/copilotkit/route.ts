import { CopilotRuntime, OpenAIAdapter, copilotRuntimeNextJSAppRouterEndpoint } from "@copilotkit/runtime";

// Use OpenAI adapter with environment variables pointing to Ollama
const openaiAdapter = new OpenAIAdapter({
  model: "gpt-oss:20b",
});

export const runtime = "nodejs";

const runtimeInstance = new CopilotRuntime({});

export const POST = async (req: Request) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime: runtimeInstance,
    serviceAdapter: openaiAdapter,
    endpoint: "/api/copilotkit",
  });
  return handleRequest(req);
};

