import { CopilotRuntime, GoogleGenerativeAIAdapter, copilotRuntimeNextJSAppRouterEndpoint } from "@copilotkit/runtime";

// Use Google Gemini adapter - this connects to your Gemini model
const geminiAdapter = new GoogleGenerativeAIAdapter({
  model: "gemini-2.0-flash-exp",
});

export const runtime = "nodejs";

const runtimeInstance = new CopilotRuntime({});

export const POST = async (req: Request) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime: runtimeInstance,
    serviceAdapter: geminiAdapter,
    endpoint: "/api/copilotkit",
  });
  return handleRequest(req);
};

