import express, { Request, Response } from "express";

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.json());

// Health check
app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// Example route
app.get("/api/greeting", (_req: Request, res: Response) => {
  const name = _req.query.name || "World";
  res.json({ message: `Hello, ${name}!` });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

export default app;
