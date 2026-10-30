import { Namespace } from '@vfs-ai/types';
import { generateNamespaceId } from '@vfs-ai/utils';

export class NamespaceManager {
  private namespaces = new Map<string, Namespace>();

  create(name: string, ownerId?: string, description?: string): Namespace {
    const ns: Namespace = {
      id: generateNamespaceId(),
      name,
      ownerId,
      description,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.namespaces.set(name, ns);
    return ns;
  }

  get(name: string): Namespace | undefined {
    return this.namespaces.get(name);
  }

  list(): Namespace[] {
    return Array.from(this.namespaces.values());
  }

  exists(name: string): boolean {
    return this.namespaces.has(name);
  }

  delete(name: string): boolean {
    return this.namespaces.delete(name);
  }
}
