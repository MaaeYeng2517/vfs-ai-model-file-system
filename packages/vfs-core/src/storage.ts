import { promises as fs } from 'fs';
import { join } from 'path';
import { sha256 } from '@vfs-ai/utils';

export class ObjectStorage {
  constructor(private basePath: string) {}

  async init(): Promise<void> {
    await fs.mkdir(this.basePath, { recursive: true });
    await fs.mkdir(join(this.basePath, 'objects'), { recursive: true });
  }

  private objectPath(hash: string): string {
    // Use first 2 chars as prefix for directory sharding
    return join(this.basePath, 'objects', hash.slice(0, 2), hash);
  }

  async put(content: Buffer): Promise<string> {
    const hash = sha256(content);
    const path = this.objectPath(hash);
    await fs.mkdir(join(path, '..'), { recursive: true });
    
    try {
      // Check if exists
      await fs.access(path);
    } catch {
      await fs.writeFile(path, content);
    }
    
    return hash;
  }

  async get(hash: string): Promise<Buffer> {
    const path = this.objectPath(hash);
    return fs.readFile(path);
  }

  async exists(hash: string): Promise<boolean> {
    try {
      await fs.access(this.objectPath(hash));
      return true;
    } catch {
      return false;
    }
  }

  async delete(hash: string): Promise<boolean> {
    try {
      await fs.unlink(this.objectPath(hash));
      return true;
    } catch {
      return false;
    }
  }
}
