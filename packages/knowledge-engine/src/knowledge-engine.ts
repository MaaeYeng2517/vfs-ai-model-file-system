import { KnowledgeDocument } from '@vfs-ai/types';
import { generateId, getExtension } from '@vfs-ai/utils';
import { VfsEngine } from '@vfs-ai/vfs-core';

export interface Chunk {
  id: string;
  documentId: string;
  content: string;
  index: number;
  metadata?: Record<string, unknown>;
}

export class KnowledgeEngine {
  private documents = new Map<string, KnowledgeDocument>();
  private chunks = new Map<string, Chunk[]>(); // documentId -> chunks

  constructor(private vfs: VfsEngine) {}

  async ingest(namespace: string, path: string, options: { chunkSize?: number } = {}): Promise<KnowledgeDocument> {
    const ext = getExtension(path);
    let sourceType: KnowledgeDocument['sourceType'] = 'other';
    
    if (ext === 'pdf') sourceType = 'pdf';
    else if (ext === 'md') sourceType = 'markdown';
    else if (ext === 'txt') sourceType = 'txt';
    else if (ext === 'html' || ext === 'htm') sourceType = 'html';

    const asset = await this.vfs.stat(namespace, path);
    if (!asset) throw new Error(`File not found in VFS: ${namespace}:${path}`);

    const content = await this.vfs.readFile(namespace, path);
    const text = content.toString('utf-8');
    
    // Simple chunking
    const chunkSize = options.chunkSize || 1000;
    const chunks: Chunk[] = [];
    for (let i = 0; i < text.length; i += chunkSize) {
      chunks.push({
        id: generateId(),
        documentId: '',
        content: text.slice(i, i + chunkSize),
        index: Math.floor(i / chunkSize),
      });
    }

    const doc: KnowledgeDocument = {
      id: generateId(),
      assetId: asset.id,
      sourceType,
      chunks: chunks.length,
      extractedAt: new Date(),
    };

    // Update chunk documentIds
    for (const chunk of chunks) {
      chunk.documentId = doc.id;
    }

    this.documents.set(doc.id, doc);
    this.chunks.set(doc.id, chunks);
    return doc;
  }

  getDocument(id: string): KnowledgeDocument | undefined {
    return this.documents.get(id);
  }

  getChunks(documentId: string): Chunk[] {
    return this.chunks.get(documentId) || [];
  }

  listDocuments(): KnowledgeDocument[] {
    return Array.from(this.documents.values());
  }
}
