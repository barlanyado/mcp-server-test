import express from "express";

const app = express();

// Serve the MCP config file from .well-known/
app.use("/.well-known", express.static(".well-known"));

// Example endpoint — your MCP capabilities would go here
app.get("/", (req, res) => {
  res.json({
    message: "Hello from my MCP server!",
    status: "ok",
  });
});

// MCP initialize endpoint (Smithery expects this)
app.post("/", (req, res) => {
  res.json({
    jsonrpc: "2.0",
    result: {
      serverInfo: { name: "mcp-server-test", version: "1.0.0" },
      capabilities: {},
    },
    id: 0
  });
});

// Start the HTTP server (port 8080 required for Smithery)
const PORT = process.env.PORT || 8080;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`✅ MCP server running on port ${PORT}`);
});
