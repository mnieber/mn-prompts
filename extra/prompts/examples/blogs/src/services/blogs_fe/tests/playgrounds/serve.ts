// Serves a playground: a FakeBackend with data, that the app uses when
// flags.useFakeBackend is true. Usage: yarn fake <playground>, e.g. yarn fake blogs/createBlog.
import fs from 'fs';
import http from 'http';
import path from 'path';
import { pathToFileURL } from 'url';
import { FakeBackend } from '/tests/fakeBackend/FakeBackend';
import { endpoints } from '/tests/fakeBackend/endpoints';
import { fakeApiPath, playgroundPort } from '/tests/fakeBackend/urls';
import type { PlaygroundT } from '/tests/playgrounds/PlaygroundT';

// The port of the vite dev server that the playground is used with
const devServerPort = 3000;

const playgroundsDir = import.meta.dirname;

function listPlaygrounds(dir = playgroundsDir): string[] {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const entryPath = path.join(dir, entry.name);
    if (entry.isDirectory()) return listPlaygrounds(entryPath);
    const name = path.relative(playgroundsDir, entryPath);
    return dir !== playgroundsDir && name.endsWith('.ts')
      ? [name.replace(/\.ts$/, '')]
      : [];
  });
}

function readBody(request: http.IncomingMessage): Promise<any> {
  return new Promise((resolve, reject) => {
    let data = '';
    request.on('data', (chunk) => (data += chunk));
    request.on('end', () => resolve(data ? JSON.parse(data) : undefined));
    request.on('error', reject);
  });
}

async function main() {
  const name = process.argv[2];
  if (!name || !listPlaygrounds().includes(name)) {
    console.log('Usage: yarn fake <playground>\n\nPlaygrounds:');
    listPlaygrounds().forEach((x) => console.log(`  ${x}`));
    process.exit(name ? 1 : 0);
  }

  const moduleUrl = pathToFileURL(path.join(playgroundsDir, `${name}.ts`));
  const { playground } = (await import(moduleUrl.href)) as {
    playground: PlaygroundT;
  };

  const backend = new FakeBackend(fakeApiPath, endpoints);
  playground.setUp(backend);

  const server = http.createServer(async (request, response) => {
    const method = request.method ?? 'GET';
    const url = request.url ?? '';
    const body = await readBody(request);
    const { status, json } = backend.respond(method, url, body);
    const endpointName = backend.requests.at(-1)?.name;

    const isUnexpected = json?.[0] === 'UNEXPECTED_REQUEST';
    console.log(
      isUnexpected
        ? `${method} ${url} → ${status} (no fake endpoint for this request)`
        : `${method} ${url} → ${status} (${endpointName})`
    );
    if (body !== undefined) console.log(`  ${JSON.stringify(body)}`);

    response.writeHead(status, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(json));
  });

  server.on('error', (error: NodeJS.ErrnoException) => {
    console.error(
      error.code === 'EADDRINUSE'
        ? `Port ${playgroundPort} is in use. Is another playground running?`
        : error
    );
    process.exit(1);
  });

  server.listen(playgroundPort, () => {
    console.log(`Playground "${name}" on :${playgroundPort}`);
    console.log(`  ${playground.description}`);
    console.log(`Open http://localhost:${devServerPort}${playground.url}`);
    console.log(
      `(this needs useFakeBackend: true in src/app/flags.ts; reload the page after switching playgrounds)\n`
    );
  });
}

main();
