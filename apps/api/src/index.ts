import { Hono } from 'hono';
import { serve } from '@hono/node-server';
import { cors } from 'hono/cors';
import { VfsEngine } from '@vfs-ai/vfs-core';
import { ModelEngine } from '@vfs-ai/model-engine';
import { DatasetEngine } from '@vfs-ai/dataset-engine';
import { VectorEngine } from '@vfs-ai/vector-engine';
import { KnowledgeEngine } from '@vfs-ai/knowledge-engine';
import { join } from 'path';

const app = new Hono();

app.use('/*', cors());

const dataDir = join(process.cwd(), '../../data');
const vfs = new VfsEngine({ dataDir });
const modelEngine = new ModelEngine(vfs);
const datasetEngine = new DatasetEngine(vfs);
const vectorEngine = new VectorEngine(vfs);
const knowledgeEngine = new KnowledgeEngine(vfs);

await vfs.init();

app.get('/', (c) => {
  return c.json({
    name: 'vfs-ai-engine',
    version: '0.0.1',
    engines: ['vfs', 'model', 'dataset', 'vector', 'knowledge'],
  });
});

app.get('/health', (c) => c.json({ status: 'ok' }));

// VFS routes
app.get('/vfs/namespaces', (c) => {
  return c.json(vfs.getNamespaceManager().list());
});

app.post('/vfs/namespaces', async (c) => {
  const body = await c.req.json();
  const ns = vfs.getNamespaceManager().create(body.name, body.ownerId, body.description);
  return c.json(ns);
});

app.get('/vfs/:namespace', async (c) => {
  const namespace = c.req.param('namespace');
  const dir = c.req.query('dir') || '';
  const list = await vfs.list(namespace, dir);
  return c.json(list);
});

app.post('/vfs/:namespace/write', async (c) => {
  const namespace = c.req.param('namespace');
  const body = await c.req.json();
  const asset = await vfs.writeFile(namespace, body.path, body.content);
  return c.json(asset);
});

app.get('/vfs/:namespace/read', async (c) => {
  const namespace = c.req.param('namespace');
  const path = c.req.query('path');
  if (!path) return c.json({ error: 'path required' }, 400);
  const content = await vfs.readFile(namespace, path);
  return c.body(content);
});

// Model routes
app.get('/models', (c) => c.json(modelEngine.list()));
app.post('/models/register', async (c) => {
  const body = await c.req.json();
  const model = await modelEngine.register(body.namespace, body.path, body.options);
  return c.json(model);
});

// Dataset routes
app.get('/datasets', (c) => c.json(datasetEngine.list()));
app.post('/datasets/register', async (c) => {
  const body = await c.req.json();
  const dataset = await datasetEngine.register(body.namespace, body.path, body.options);
  return c.json(dataset);
});

// Vector routes
app.get('/vectors/collections', (c) => c.json(vectorEngine.listCollections()));
app.post('/vectors/collections', async (c) => {
  const body = await c.req.json();
  const collection = await vectorEngine.createCollection(body.namespace, body.name, body.options);
  return c.json(collection);
});
app.post('/vectors/:id/search', async (c) => {
  const id = c.req.param('id');
  const body = await c.req.json();
  const results = await vectorEngine.search(id, body.query, body.topK);
  return c.json(results);
});

// Knowledge routes
app.get('/knowledge/documents', (c) => c.json(knowledgeEngine.listDocuments()));
app.post('/knowledge/ingest', async (c) => {
  const body = await c.req.json();
  const doc = await knowledgeEngine.ingest(body.namespace, body.path, body.options);
  return c.json(doc);
});

const port = Number(process.env.PORT) || 3000;
console.log(`Server running on http://localhost:${port}`);
serve({ fetch: app.fetch, port });
