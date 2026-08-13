#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

function fail(message) {
  process.stdout.write(`${JSON.stringify({ error: message })}\n`);
  process.exit(1);
}

function mutateValue(value, marker) {
  if (typeof value === 'number' && Number.isFinite(value)) return value + marker;
  if (typeof value === 'string') return `${value}__vm_probe_${marker}`;
  if (typeof value === 'boolean') return !value;
  if (value === null || value === undefined) return marker;
  return value;
}

function mutateAtPath(root, pathValue, marker) {
  const segments = pathValue.replace(/\[\]/g, '.[]').split('.').filter(Boolean);
  function visit(value, index) {
    if (index >= segments.length) return mutateValue(value, marker);
    const segment = segments[index];
    if (segment === '[]') {
      if (!Array.isArray(value)) return value;
      return value.map((item) => visit(item, index + 1));
    }
    if (!value || typeof value !== 'object') return value;
    if (Object.prototype.hasOwnProperty.call(value, segment)) {
      value[segment] = visit(value[segment], index + 1);
    }
    return value;
  }
  visit(root, 0);
}

function execute(source, responses, timeout) {
  const responseJson = JSON.stringify(responses).replace(/</g, '\\u003c');
  const program = `
    "use strict";
    const responses = JSON.parse(${JSON.stringify(responseJson)});
    const transform = (${source});
    const output = transform(responses);
    JSON.parse(JSON.stringify(output));
  `;
  const context = vm.createContext(Object.create(null), {
    codeGeneration: { strings: false, wasm: false },
  });
  return vm.runInContext(program, context, { timeout });
}

let payload;
try {
  payload = JSON.parse(readFileSync(0, 'utf8'));
} catch {
  fail('无法读取 transform 隔离执行输入');
}

try {
  const timeout = Number.isInteger(payload.timeout) ? payload.timeout : 500;
  const baseline = execute(payload.source, payload.responses, timeout);
  const probes = [];
  for (const probe of payload.probes || []) {
    const responses = structuredClone(payload.responses);
    mutateAtPath(responses[probe.requestId], probe.path, probe.marker);
    probes.push({ id: probe.id, output: execute(payload.source, responses, timeout) });
  }
  process.stdout.write(`${JSON.stringify({ baseline, probes })}\n`);
} catch (error) {
  fail(error && error.message ? error.message : 'transform 隔离执行失败');
}
