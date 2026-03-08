/**
 * Module B: File Processing Service
 * Legacy module using callback patterns — for migration exercise.
 */

import * as fs from 'fs';
import * as path from 'path';

interface FileInfo {
  name: string;
  path: string;
  size: number;
  extension: string;
  modifiedAt: Date;
}

interface ProcessingResult {
  file: string;
  status: 'success' | 'error';
  output?: string;
  error?: string;
  duration: number;
}

type Callback<T> = (error: Error | null, result?: T) => void;

/**
 * Read a file and return its info.
 * Uses callback pattern (should be migrated to async/await).
 */
export function getFileInfo(
  filePath: string,
  callback: Callback<FileInfo>
): void {
  fs.stat(filePath, (err, stats) => {
    if (err) {
      callback(new Error(`Cannot access file: ${filePath}`));
      return;
    }

    const info: FileInfo = {
      name: path.basename(filePath),
      path: filePath,
      size: stats.size,
      extension: path.extname(filePath),
      modifiedAt: stats.mtime,
    };

    callback(null, info);
  });
}

/**
 * Process a file by reading and transforming its content.
 * Uses callback pattern with nested callbacks.
 */
export function processFile(
  filePath: string,
  transform: (content: string) => string,
  callback: Callback<ProcessingResult>
): void {
  const startTime = Date.now();

  // Step 1: Check file exists
  fs.access(filePath, fs.constants.R_OK, (err) => {
    if (err) {
      callback(null, {
        file: filePath,
        status: 'error',
        error: 'File not accessible',
        duration: Date.now() - startTime,
      });
      return;
    }

    // Step 2: Read file
    fs.readFile(filePath, 'utf-8', (readErr, content) => {
      if (readErr) {
        callback(null, {
          file: filePath,
          status: 'error',
          error: `Read error: ${readErr.message}`,
          duration: Date.now() - startTime,
        });
        return;
      }

      // Step 3: Transform
      try {
        const transformed = transform(content);

        // Step 4: Write result
        const outputPath = filePath + '.processed';
        fs.writeFile(outputPath, transformed, 'utf-8', (writeErr) => {
          if (writeErr) {
            callback(null, {
              file: filePath,
              status: 'error',
              error: `Write error: ${writeErr.message}`,
              duration: Date.now() - startTime,
            });
            return;
          }

          callback(null, {
            file: filePath,
            status: 'success',
            output: outputPath,
            duration: Date.now() - startTime,
          });
        });
      } catch (transformErr: any) {
        callback(null, {
          file: filePath,
          status: 'error',
          error: `Transform error: ${transformErr.message}`,
          duration: Date.now() - startTime,
        });
      }
    });
  });
}

/**
 * Process multiple files sequentially.
 * Uses recursive callback pattern (should be migrated to async/await with Promise.all).
 */
export function processMultipleFiles(
  filePaths: string[],
  transform: (content: string) => string,
  callback: Callback<ProcessingResult[]>
): void {
  const results: ProcessingResult[] = [];
  let index = 0;

  function processNext(): void {
    if (index >= filePaths.length) {
      callback(null, results);
      return;
    }

    const currentFile = filePaths[index];
    index++;

    processFile(currentFile, transform, (err, result) => {
      if (err) {
        results.push({
          file: currentFile,
          status: 'error',
          error: err.message,
          duration: 0,
        });
      } else if (result) {
        results.push(result);
      }

      processNext();
    });
  }

  processNext();
}

/**
 * Watch a directory for file changes.
 * Uses callback for each change event.
 */
export function watchDirectory(
  dirPath: string,
  callback: Callback<{ event: string; filename: string }>
): fs.FSWatcher | null {
  try {
    const watcher = fs.watch(dirPath, (eventType, filename) => {
      if (filename) {
        callback(null, { event: eventType, filename });
      }
    });

    watcher.on('error', (err) => {
      callback(new Error(`Watcher error: ${err.message}`));
    });

    return watcher;
  } catch (err: any) {
    callback(new Error(`Cannot watch directory: ${err.message}`));
    return null;
  }
}

/**
 * Copy a file with progress reporting.
 * Uses callback pattern with progress events.
 */
export function copyFileWithProgress(
  source: string,
  destination: string,
  onProgress: (percent: number) => void,
  callback: Callback<void>
): void {
  fs.stat(source, (err, stats) => {
    if (err) {
      callback(new Error(`Source not found: ${source}`));
      return;
    }

    const totalSize = stats.size;
    let copiedSize = 0;

    const readStream = fs.createReadStream(source);
    const writeStream = fs.createWriteStream(destination);

    readStream.on('data', (chunk: Buffer) => {
      copiedSize += chunk.length;
      const percent = Math.round((copiedSize / totalSize) * 100);
      onProgress(percent);
    });

    readStream.on('error', (readErr) => {
      callback(new Error(`Read error: ${readErr.message}`));
    });

    writeStream.on('error', (writeErr) => {
      callback(new Error(`Write error: ${writeErr.message}`));
    });

    writeStream.on('finish', () => {
      callback(null);
    });

    readStream.pipe(writeStream);
  });
}
