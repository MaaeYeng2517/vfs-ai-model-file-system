import { VectorCollection } from '@vfs-ai/types';
import { generateId } from '@vfs-ai/utils';
import { VfsEngine } from '@vfs-ai/vfs-core';

export interface Vector {
  id: string;
  values: number[];
  metadata?: Record<string, unknown>;
}

export class VectorEngine {
  private collections = new Map<string, VectorCollection>();
  private vectors = new Map<string, Vector[]>(); // collectionId -> vectors

  constructor(private vfs: VfsEngine) {}

  async createCollection(
    namespace: string, 
    name: string, 
    options: {
      dimension: number;
      metric?: VectorCollection['metric'];
      indexType?: VectorCollection['indexType'];
    }
  ): Promise<VectorCollection> {
    const asset = await this.vfs.writeFile(namespace, `vectors/${name}/collection.json`, 
      JSON.stringify({ ...options, createdAt: new Date().toISOString() }, null, 2)
    );

    const collection: VectorCollection = {
      id: generateId(),
      assetId: asset.id,
      dimension: options.dimension,
      metric: options.metric || 'cosine',
      indexType: options.indexType || 'hnsw',
      count: 0,
    };

    this.collections.set(collection.id, collection);
    this.vectors.set(collection.id, []);
    return collection;
  }

  async upsert(collectionId: string, vectors: Vector[]): Promise<number> {
    const collection = this.collections.get(collectionId);
    if (!collection) throw new Error('Collection not found');
    
    const existing = this.vectors.get(collectionId) || [];
    for (const v of vectors) {
      if (v.values.length !== collection.dimension) {
        throw new Error(`Vector dimension mismatch: expected ${collection.dimension}, got ${v.values.length}`);
      }
      existing.push(v);
    }
    
    this.vectors.set(collectionId, existing);
    collection.count = existing.length;
    return vectors.length;
  }

  async search(collectionId: string, query: number[], topK: number = 10): Promise<Array<{ id: string; score: number; metadata?: Record<string, unknown> }>> {
    const collection = this.collections.get(collectionId);
    if (!collection) throw new Error('Collection not found');
    
    if (query.length !== collection.dimension) {
      throw new Error(`Query dimension mismatch`);
    }

    const vectors = this.vectors.get(collectionId) || [];
    // Simple cosine similarity for now
    const results = vectors.map(v => {
      let score = 0;
      if (collection.metric === 'cosine') {
        let dot = 0, normA = 0, normB = 0;
        for (let i = 0; i < query.length; i++) {
          dot += query[i] * v.values[i];
          normA += query[i] * query[i];
          normB += v.values[i] * v.values[i];
        }
        score = dot / (Math.sqrt(normA) * Math.sqrt(normB));
      }
      return { id: v.id, score, metadata: v.metadata };
    });

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  }

  getCollection(id: string): VectorCollection | undefined {
    return this.collections.get(id);
  }

  listCollections(): VectorCollection[] {
    return Array.from(this.collections.values());
  }
}
