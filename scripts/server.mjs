import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const port = Number(process.env.PORT || 4173);
const types = new Map([
  [".html", "text/html; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".svg", "image/svg+xml; charset=utf-8"]
]);

function resolvePath(urlPath) {
  const clean = decodeURIComponent(urlPath.split("?")[0]);
  let target = clean === "/" ? "/index.html" : clean;
  if (target === "/review") target = "/review/index.html";
  const full = path.normalize(path.join(root, target));
  if (!full.startsWith(root)) return null;
  if (fs.existsSync(full) && fs.statSync(full).isDirectory()) return path.join(full, "index.html");
  return full;
}

const server = http.createServer((req, res) => {
  const file = resolvePath(req.url || "/");
  if (!file || !fs.existsSync(file)) {
    res.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    res.end("Not found");
    return;
  }
  res.writeHead(200, { "content-type": types.get(path.extname(file)) || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});

server.listen(port, () => {
  console.log(`DPI-HT-01 app running at http://localhost:${port}`);
});
