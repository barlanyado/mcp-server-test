import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());

app.use("/.well-known", express.static(path.join(__dirname, ".well-known")));

app.get("/", (req, res) => {
  res.json({ status: "ok", message: "MCP server online" });
});

// Handle MCP JSON-RPC requests
app.post("/", (req, res) => {
  const { method, id } = req.body;

  // MCP "initialize" handshake
  if (method === "initialize") {
    return res.json({
      jsonrpc: "2.0",
      id,
      result: {
        serverInfo: { name: "mcp-server-test", version: "1.0.0" },
        capabilities: {
          tools: {
            sayHello: {
              name: "sayHello",
              description: "Returns the phrase 'say hello'",
              inputSchema: { type: "object", properties: {} }
            }
          }
        }
      }
    });
  }

  // MCP "tools/call" — when a tool is invoked
  if (method === "tools/call") {
    const { name } = req.body.params || {};

    if (name === "sayHello") {
      return res.json({
        jsonrpc: "2.0",
        id,
        result: {
          content: [
            {
              type: "text",
              text: "say hello"
            }
          ]
        }
      });
    }

    return res.json({
      jsonrpc: "2.0",
      id,
      error: { code: -32601, message: `Unknown tool: ${name}` }
    });
  }

  // Fallback for unknown methods
  res.json({
    jsonrpc: "2.0",
    id,
    error: { code: -32601, message: "Unknown method"
