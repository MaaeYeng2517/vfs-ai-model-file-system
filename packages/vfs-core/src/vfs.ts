import { promises as fs } from 'fs';
import { join, dirname } from 'path';
import { AssetMetadata, AssetType } from '@vfs-ai/types';
import { generateAssetId, normalizePath, buildVfsUri, sha256 } from '@vfs-ai/utils';
import { NamespaceManager } from './namespace.js';
import { ObjectStorage } from './storage.js';

export interface VfsOptions {
  dataDir: string;
}

export class VfsEngine {
  private nsManager: NamespaceManager;
  private storage: ObjectStorage;
  private metadata = new Map<string, AssetMetadata>(); // key: namespace/path
  private metaDir: string;

  constructor(private options: VfsOptions) {
    this.nsManager = new NamespaceManager();
    this.storage = new ObjectStorage(join(options.dataDir, 'storage'));
    this.metaDir = join(options.dataDir, 'metadata');
  }

  async init(): Promise<void> {
    await this.storage.init();
    await fs.mkdir(this.metaDir, { recursive: true });
    // Create default namespace
    if (!this.nsManager.exists('default')) {
      this.nsManager.create('default', undefined, 'Default namespace');
    }
  }

  private metaKey(namespace: string, path: string): string {
    return `${namespace}:${normalizePath(path)}`;
  }

  async createDirectory(namespace: string, path: string): Promise<AssetMetadata> {
    if (!this.nsManager.exists(namespace)) {
      throw new Error(`Namespace not found: ${namespace}`);
    }

    const normalizedPath = normalizePath(path);
    if (!normalizedPath) throw new Error('Path cannot be empty');

    const key = this.metaKey(namespace, normalizedPath);
    const asset: AssetMetadata = {
      id: generateAssetId(),
      type: 'directory',
      namespace,
      path: normalizedPath,
      uri: buildVfsUri(namespace, normalizedPath),
      name: normalizedPath.split('/').pop() || normalizedPath,
      tags: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.metadata.set(key, asset);
    return asset;
  }

  async writeFile(namespace: string, path: string, content: Buffer | string): Promise<AssetMetadata> {
    if (!this.nsManager.exists(namespace)) {
      throw new Error(`Namespace not found: ${namespace}`);
    }

    const normalizedPath = normalizePath(path);
    if (!normalizedPath) throw new Error('Path cannot be empty');

    const buf = typeof content === 'string' ? Buffer.from(content) : content;
    const hash = await this.storage.put(buf);

    const key = this.metaKey(namespace, normalizedPath);
    const asset: AssetMetadata = {
      id: generateAssetId(),
      type: 'file',
      namespace,
      path: normalizedPath,
      uri: buildVfsUri(namespace, normalizedPath),
      name: normalizedPath.split('/').pop() || normalizedPath,
      size: buf.length,
      hash,
      tags: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.metadata.set(key, asset);
    return asset;
  }

  async readFile(namespace: string, path: string): Promise<Buffer> {
    const normalizedPath = normalizePath(path);
    const key = this.metaKey(namespace, normalizedPath);
    const meta = this.metadata.get(key);

    if (!meta || !meta.hash) {
      throw new Error(`File not found: ${namespace}:${normalizedPath}`);
    }

    return this.storage.get(meta.hash);
  }

  async stat(namespace: string, path: string): Promise<AssetMetadata | undefined> {
    const normalizedPath = normalizePath(path);
    const key = this.metaKey(namespace, normalizedPath);
    return this.metadata.get(key);
  }

  async list(namespace: string, dirPath: string = ''): Promise<AssetMetadata[]> {
    const normalizedDir = normalizePath(dirPath);
    const results: AssetMetadata[] = [];

    for (const asset of this.metadata.values()) {
      if (asset.namespace !== namespace) continue;
      if (normalizedDir === '') {
        // List top level
        if (!asset.path.includes('/')) {
          results.push(asset);
        }
      } else {
        if (asset.path.startsWith(normalizedDir + '/') && 
            !asset.path.slice(normalizedDir.length + 1).includes('/')) {
          results.push(asset);
        }
      }
    }

    return results;
  }

  async exists(namespace: string, path: string): Promise<boolean> {
    const normalizedPath = normalizePath(path);
    const key = this.metaKey(namespace, normalizedPath);
    return this.metadata.has(key);
  }

  getNamespaceManager(): NamespaceManager {
    return this.nsManager;
  }
}
