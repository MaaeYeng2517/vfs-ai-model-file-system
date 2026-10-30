import { Dataset } from '@vfs-ai/types';
import { generateId, getExtension } from '@vfs-ai/utils';
import { VfsEngine } from '@vfs-ai/vfs-core';

export class DatasetEngine {
  private datasets = new Map<string, Dataset>();

  constructor(private vfs: VfsEngine) {}

  async register(namespace: string, path: string, options: Partial<Dataset> = {}): Promise<Dataset> {
    const ext = getExtension(path);
    let format: Dataset['format'] = 'other';
    
    if (ext === 'jsonl') format = 'jsonl';
    else if (ext === 'csv') format = 'csv';
    else if (ext === 'parquet') format = 'parquet';
    else if (ext === 'arrow') format = 'arrow';

    const asset = await this.vfs.stat(namespace, path);
    if (!asset) throw new Error(`File not found in VFS: ${namespace}:${path}`);

    const dataset: Dataset = {
      id: generateId(),
      assetId: asset.id,
      schema: options.schema || {},
      version: options.version || '1.0.0',
      splits: options.splits || {},
      rowCount: options.rowCount,
      format,
    };

    this.datasets.set(dataset.id, dataset);
    return dataset;
  }

  get(id: string): Dataset | undefined {
    return this.datasets.get(id);
  }

  list(): Dataset[] {
    return Array.from(this.datasets.values());
  }

  async version(datasetId: string, newVersion: string): Promise<Dataset> {
    const existing = this.datasets.get(datasetId);
    if (!existing) throw new Error('Dataset not found');
    
    const versioned: Dataset = {
      ...existing,
      id: generateId(),
      version: newVersion,
    };
    
    this.datasets.set(versioned.id, versioned);
    return versioned;
  }
}
