#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';
import { VfsEngine } from '@vfs-ai/vfs-core';
import { ModelEngine } from '@vfs-ai/model-engine';
import { DatasetEngine } from '@vfs-ai/dataset-engine';
import { VectorEngine } from '@vfs-ai/vector-engine';
import { KnowledgeEngine } from '@vfs-ai/knowledge-engine';
import { join } from 'path';

const program = new Command();

const dataDir = join(process.cwd(), 'data');
const vfs = new VfsEngine({ dataDir });
const modelEngine = new ModelEngine(vfs);
const datasetEngine = new DatasetEngine(vfs);
const vectorEngine = new VectorEngine(vfs);
const knowledgeEngine = new KnowledgeEngine(vfs);

program
  .name('vfs')
  .description('VFS-AI-Engine CLI')
  .version('0.0.1');

program
  .command('init')
  .description('Initialize VFS-AI-Engine')
  .action(async () => {
    await vfs.init();
    console.log(chalk.green('✓ VFS-AI-Engine initialized'));
    console.log(chalk.gray(`  Data directory: ${dataDir}`));
  });

program
  .command('ns:create <name>')
  .description('Create namespace')
  .option('-d, --desc <desc>', 'Description')
  .action(async (name, options) => {
    await vfs.init();
    const ns = vfs.getNamespaceManager().create(name, undefined, options.desc);
    console.log(chalk.green('✓ Namespace created'));
    console.log(chalk.gray(`  ID: ${ns.id}`));
    console.log(chalk.gray(`  Name: ${ns.name}`));
  });

program
  .command('ns:list')
  .description('List namespaces')
  .action(async () => {
    await vfs.init();
    const list = vfs.getNamespaceManager().list();
    console.log(chalk.cyan(`Namespaces (${list.length}):`));
    for (const ns of list) {
      console.log(`  ${chalk.bold(ns.name)} ${chalk.gray(`(${ns.id})`)}`);
      if (ns.description) console.log(`    ${chalk.gray(ns.description)}`);
    }
  });

program
  .command('fs:write <namespace> <path> <content>')
  .description('Write file to VFS')
  .action(async (namespace, path, content) => {
    await vfs.init();
    const asset = await vfs.writeFile(namespace, path, content);
    console.log(chalk.green('✓ File written'));
    console.log(chalk.gray(`  URI: ${asset.uri}`));
    console.log(chalk.gray(`  Hash: ${asset.hash?.slice(0, 16)}...`));
    console.log(chalk.gray(`  Size: ${asset.size} bytes`));
  });

program
  .command('fs:read <namespace> <path>')
  .description('Read file from VFS')
  .action(async (namespace, path) => {
    await vfs.init();
    const content = await vfs.readFile(namespace, path);
    console.log(content.toString());
  });

program
  .command('fs:ls [namespace] [dir]')
  .description('List files')
  .action(async (namespace = 'default', dir = '') => {
    await vfs.init();
    const list = await vfs.list(namespace, dir);
    console.log(chalk.cyan(`Files in ${namespace}:${dir || '/'} (${list.length}):`));
    for (const asset of list) {
      const icon = asset.type === 'directory' ? '📁' : '📄';
      console.log(`  ${icon} ${asset.name} ${chalk.gray(`(${asset.id})`)}`);
    }
  });

program
  .command('model:register <namespace> <path>')
  .description('Register AI model')
  .option('-v, --version <ver>', 'Version', '1.0.0')
  .option('-q, --quant <quant>', 'Quantization')
  .action(async (namespace, path, options) => {
    await vfs.init();
    const model = await modelEngine.register(namespace, path, options);
    console.log(chalk.green('✓ Model registered'));
    console.log(chalk.gray(`  ID: ${model.id}`));
    console.log(chalk.gray(`  Framework: ${model.framework}`));
    console.log(chalk.gray(`  Version: ${model.version}`));
  });

program
  .command('model:list')
  .description('List models')
  .action(async () => {
    const list = modelEngine.list();
    console.log(chalk.cyan(`Models (${list.length}):`));
    for (const model of list) {
      console.log(`  🤖 ${model.id} ${chalk.gray(`(${model.framework} v${model.version})`)}`);
    }
  });

program
  .command('dataset:register <namespace> <path>')
  .description('Register dataset')
  .option('-v, --version <ver>', 'Version', '1.0.0')
  .action(async (namespace, path, options) => {
    await vfs.init();
    const dataset = await datasetEngine.register(namespace, path, options);
    console.log(chalk.green('✓ Dataset registered'));
    console.log(chalk.gray(`  ID: ${dataset.id}`));
    console.log(chalk.gray(`  Format: ${dataset.format}`));
    console.log(chalk.gray(`  Version: ${dataset.version}`));
  });

program
  .command('dataset:list')
  .description('List datasets')
  .action(async () => {
    const list = datasetEngine.list();
    console.log(chalk.cyan(`Datasets (${list.length}):`));
    for (const dataset of list) {
      console.log(`  📊 ${dataset.id} ${chalk.gray(`(${dataset.format} v${dataset.version})`)}`);
    }
  });

program
  .command('vector:create <namespace> <name>')
  .description('Create vector collection')
  .option('-d, --dim <dim>', 'Dimension', '384')
  .option('-m, --metric <metric>', 'Metric', 'cosine')
  .action(async (namespace, name, options) => {
    await vfs.init();
    const collection = await vectorEngine.createCollection(namespace, name, {
      dimension: parseInt(options.dim),
      metric: options.metric,
    });
    console.log(chalk.green('✓ Vector collection created'));
    console.log(chalk.gray(`  ID: ${collection.id}`));
    console.log(chalk.gray(`  Dimension: ${collection.dimension}`));
    console.log(chalk.gray(`  Metric: ${collection.metric}`));
  });

program
  .command('vector:list')
  .description('List vector collections')
  .action(async () => {
    const list = vectorEngine.listCollections();
    console.log(chalk.cyan(`Vector collections (${list.length}):`));
    for (const col of list) {
      console.log(`  🔍 ${col.id} ${chalk.gray(`(dim:${col.dimension}, ${col.metric}, count:${col.count})`)}`);
    }
  });

program
  .command('knowledge:ingest <namespace> <path>')
  .description('Ingest document into knowledge base')
  .option('-c, --chunk <size>', 'Chunk size', '1000')
  .action(async (namespace, path, options) => {
    await vfs.init();
    const doc = await knowledgeEngine.ingest(namespace, path, {
      chunkSize: parseInt(options.chunk),
    });
    console.log(chalk.green('✓ Document ingested'));
    console.log(chalk.gray(`  ID: ${doc.id}`));
    console.log(chalk.gray(`  Source: ${doc.sourceType}`));
    console.log(chalk.gray(`  Chunks: ${doc.chunks}`));
  });

program
  .command('knowledge:list')
  .description('List knowledge documents')
  .action(async () => {
    const list = knowledgeEngine.listDocuments();
    console.log(chalk.cyan(`Knowledge documents (${list.length}):`));
    for (const doc of list) {
      console.log(`  📚 ${doc.id} ${chalk.gray(`(${doc.sourceType}, ${doc.chunks} chunks)`)}`);
    }
  });

program.parse();
