// Generate a valid UUID v4 and print it to stdout.
// Usage: node "<skill_dir>/scripts/gen-uuid.js"
// Avoid inline shell/script UUID generation; it can trigger approval prompts.
const crypto = require('crypto');
console.log(crypto.randomUUID());
