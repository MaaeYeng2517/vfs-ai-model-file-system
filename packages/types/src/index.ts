// Core types for VFS-AI-Engine

export type AssetType = 
  | 'file'
  | 'directory'
  | 'model'
  | 'dataset'
  | 'vector-index'
  | 'document'
  | 'knowledge-node';

export interface AssetMetadata {
  id: string;
  type: AssetType;
  namespace: string;
  path: string;
  uri: string; // vfs://namespace/path
  name: string;
  size?: number;
  mimeType?: string;
  hash?: string; // sha256
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  parentId?: string;
}

export interface Namespace {
  id: string;
  name: string;
  ownerId?: string;
  description?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ModelArtifact {
  id: string;
  assetId: string;
  framework: 'pytorch' | 'onnx' | 'gguf' | 'safetensors' | 'tensorflow' | 'other';
  format: string;
  version: string;
  quantization?: string;
  config?: Record<string, unknown>;
  tokenizerPath?: string;
}

export interface Dataset {
  id: string;
  assetId: string;
  schema: Record<string, unknown>;
  version: string;
  splits: {
    train?: string;
    val?: string;
    test?: string;
  };
  rowCount?: number;
  format: 'jsonl' | 'csv' | 'parquet' | 'arrow' | 'other';
}

export interface VectorCollection {
  id: string;
  assetId: string;
  dimension: number;
  metric: 'cosine' | 'euclidean' | 'dot';
  indexType: 'hnsw' | 'ivf' | 'flat';
  count: number;
}

export interface KnowledgeDocument {
  id: string;
  assetId: string;
  sourceType: 'pdf' | 'markdown' | 'txt' | 'html' | 'web' | 'other';
  chunks: number;
  language?: string;
  extractedAt: Date;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}
