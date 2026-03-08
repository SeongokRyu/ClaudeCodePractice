/**
 * Deep Merge Utility
 *
 * This function looks correct and handles nested objects well.
 * However, it contains a subtle security vulnerability:
 * Prototype Pollution.
 *
 * An attacker can inject properties into Object.prototype
 * by passing keys like "__proto__" or "constructor".
 */

type NestedObject = { [key: string]: unknown };

/**
 * Deep merges two objects together.
 * Properties from source override those in target.
 *
 * WARNING: This implementation is INTENTIONALLY VULNERABLE
 * to Prototype Pollution for educational purposes.
 */
export function deepMerge(target: NestedObject, source: NestedObject): NestedObject {
  const result: NestedObject = { ...target };

  for (const key of Object.keys(source)) {
    const sourceVal = source[key];
    const targetVal = result[key];

    // This looks reasonable — recursively merge nested objects
    if (
      sourceVal &&
      typeof sourceVal === "object" &&
      !Array.isArray(sourceVal) &&
      targetVal &&
      typeof targetVal === "object" &&
      !Array.isArray(targetVal)
    ) {
      result[key] = deepMerge(targetVal as NestedObject, sourceVal as NestedObject);
    } else {
      // BUG: No check for dangerous keys like "__proto__" or "constructor"
      // This allows Prototype Pollution attacks!
      result[key] = sourceVal;
    }
  }

  return result;
}

/**
 * Applies user-provided configuration on top of defaults.
 * Uses deepMerge internally — inherits the vulnerability.
 */
export function applyConfig(
  defaults: NestedObject,
  userConfig: NestedObject
): NestedObject {
  return deepMerge(defaults, userConfig);
}

/**
 * Processes user input and merges it with existing data.
 * In a real app, this might process API request bodies.
 */
export function processUserInput(
  existingData: NestedObject,
  userInput: string
): NestedObject {
  try {
    const parsed = JSON.parse(userInput);
    return deepMerge(existingData, parsed);
  } catch {
    throw new Error("Invalid JSON input");
  }
}

// --- Safe version (for comparison after the exercise) ---

/**
 * Safe deep merge that prevents Prototype Pollution.
 * This is the CORRECT way to implement deep merge.
 */
export function safeDeepMerge(
  target: NestedObject,
  source: NestedObject
): NestedObject {
  const result: NestedObject = { ...target };
  const DANGEROUS_KEYS = new Set(["__proto__", "constructor", "prototype"]);

  for (const key of Object.keys(source)) {
    // Guard against Prototype Pollution
    if (DANGEROUS_KEYS.has(key)) {
      continue;
    }

    // Additional check: ensure key is an own property
    if (!Object.prototype.hasOwnProperty.call(source, key)) {
      continue;
    }

    const sourceVal = source[key];
    const targetVal = result[key];

    if (
      sourceVal &&
      typeof sourceVal === "object" &&
      !Array.isArray(sourceVal) &&
      targetVal &&
      typeof targetVal === "object" &&
      !Array.isArray(targetVal)
    ) {
      result[key] = safeDeepMerge(
        targetVal as NestedObject,
        sourceVal as NestedObject
      );
    } else {
      result[key] = sourceVal;
    }
  }

  return result;
}
