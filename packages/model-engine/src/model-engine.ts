import { ModelArtifact } from '@vfs-ai/types';
import { generateId, getExtension } from '@vfs-ai/utils';
import { VfsEngine } from '@vfs-ai/vfs-core';

export class ModelEngine {
  private models = new Map<string, ModelArtifact>();

  constructor(private vfs: VfsEngine) {}

  async register(namespace: string, path: string, options: Partial<ModelArtifact> = {}): Promise<ModelArtifact> {
    const ext = getExtension(path);
    let framework: ModelArtifact['framework'] = 'other';
    
    if (ext === 'gguf') framework = 'gguf';
    else if (ext === 'safetensors') framework = 'safetensors';
    else if (ext === 'pt' || ext === 'pth') framework = 'pytorch';
    else if (ext === 'onnx') framework = 'onnx';
    else if (ext === 'pb') framework = 'tensorflow';

    const asset = await this.vfs.stat(namespace, path);
    if (!asset) throw new Error(`File not found in VFS: ${namespace}:${path}`);

    const model: ModelArtifact = {
      id: generateId(),
      assetId: asset.id,
      framework,
      format: ext || 'unknown',
      version: options.version || '1.0.0',
      quantization: options.quantization,
      config: options.config,
      tokenizerPath: options.tokenizerPath,
    };

    this.models.set(model.id, model);
    return model;
  }

  get(id: string): ModelArtifact | undefined {
    return this.models.get(id);
  }

  list(): ModelArtifact[] {
    return Array.from(this.models.values());
  }
}
