import { nanoid } from 'nanoid';
import { createHash } from 'crypto';

export function generateId(): string {
  return nanoid(12);
}

export function generateAssetId(): string {
  return `ast_${nanoid(16)}`;
}

export function generateNamespaceId(): string {
  return `ns_${nanoid(10)}`;
}

export function sha256(content: Buffer | string): string {
  const hash = createHash('sha256');
  hash.update(content);
  return hash.digest('hex');
}

export function normalizePath(path: string): string {
  // Remove leading/trailing slashes, collapse multiple slashes
  return path.replace(/\\/g, '/').replace(/\/+/g, '/').replace(/^\/|\/$/g, '');
}

export function buildVfsUri(namespace: string, path: string): string {
  const normalized = normalizePath(path);
  return normalized ? `vfs://${namespace}/${normalized}` : `vfs://${namespace}/`;
}

export function parseVfsUri(uri: string): { namespace: string; path: string } | null {
  const match = uri.match(/^vfs:\/\/([^/]+)\/?(.*)$/);
  if (!match) return null;
  return {
    namespace: match[1],
    path: normalizePath(match[2] || ''),
  };
}

export function getExtension(filename: string): string {
  const parts = filename.split('.');
  return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : '';
}

export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
