import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');
const dbKnowledgeDir = path.join(rootDir, 'database-knowledge');

const VALID_TYPES = [
  'overview', 'domain', 'object', 'metric', 'table',
  'lineage', 'sql', 'rule', 'learning', 'evidence', 'inbox'
];

const VALID_STATUSES = [
  'confirmed', 'supported', 'inferred', 'conflicted', 'open'
];

const VALID_EVIDENCE_LEVELS = ['E1', 'E2', 'E3', 'E4', 'I'];

function getAllMdFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      getAllMdFiles(filePath, fileList);
    } else if (file.endsWith('.md')) {
      fileList.push(filePath);
    }
  }
  return fileList;
}

export function parseFrontMatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) {
    return { error: 'Front Matter header missing or invalid format (must start with --- and end with ---)' };
  }

  const yamlStr = match[1];
  const data = {
    hasSourcesKey: false,
    sourcesList: []
  };

  const lines = yamlStr.split('\n');
  let currentKey = null;
  let currentSourceItem = null;

  for (let line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    const topKeyMatch = line.match(/^([a-zA-Z0-9_]+):\s*(.*)$/);
    if (topKeyMatch && !line.startsWith(' ') && !line.startsWith('\t')) {
      const key = topKeyMatch[1];
      const val = topKeyMatch[2].trim();
      currentKey = key;
      if (key === 'sources') {
        data.hasSourcesKey = true;
      } else if (val) {
        if (key === 'confidence') {
          data[key] = parseInt(val, 10);
        } else {
          data[key] = val;
        }
      }
      continue;
    }

    if (currentKey === 'sources') {
      if (trimmed.startsWith('- ')) {
        if (currentSourceItem && (currentSourceItem.path || currentSourceItem.level || currentSourceItem.location)) {
          data.sourcesList.push(currentSourceItem);
        }
        currentSourceItem = { path: '', level: '', location: '' };
        const rest = trimmed.substring(2).trim();
        const subMatch = rest.match(/^([a-zA-Z0-9_]+):\s*(.*)$/);
        if (subMatch) {
          currentSourceItem[subMatch[1]] = subMatch[2].trim();
        }
      } else if (currentSourceItem) {
        const subMatch = trimmed.match(/^([a-zA-Z0-9_]+):\s*(.*)$/);
        if (subMatch) {
          currentSourceItem[subMatch[1]] = subMatch[2].trim();
        }
      }
    }
  }

  if (currentSourceItem && (currentSourceItem.path || currentSourceItem.level || currentSourceItem.location)) {
    data.sourcesList.push(currentSourceItem);
  }

  return { data, yamlStr };
}

function checkSqlStatement(sqlText, errors, contextSnippet) {
  // Forbidden write operations
  const forbiddenWriteRegex = /\b(INSERT INTO|UPDATE\s+\w+\s+SET|DELETE FROM|DROP TABLE|ALTER TABLE|TRUNCATE TABLE|MERGE INTO)\b/i;
  if (forbiddenWriteRegex.test(sqlText)) {
    errors.push(`[SQL Safety Error] Found write/modification SQL operation in (${contextSnippet}): '${sqlText.trim().substring(0, 80)}...'`);
  }

  // ROWNUM / LIMIT <= 20 check for queries
  const rownumMatch = sqlText.match(/\bROWNUM\s*(?:<=|<|=)\s*(\d+)/i);
  if (rownumMatch) {
    const num = parseInt(rownumMatch[1], 10);
    if (num > 20) {
      errors.push(`[SQL Limit Error] ROWNUM limit ${num} in (${contextSnippet}) exceeds maximum allowed sample limit of 20`);
    }
  }

  const limitMatch = sqlText.match(/\bLIMIT\s+(\d+)/i);
  if (limitMatch) {
    const num = parseInt(limitMatch[1], 10);
    if (num > 20) {
      errors.push(`[SQL Limit Error] LIMIT ${num} in (${contextSnippet}) exceeds maximum allowed sample limit of 20`);
    }
  }
}

export function validateFile(filePath) {
  const errors = [];
  const relativePath = path.relative(rootDir, filePath);
  const content = fs.readFileSync(filePath, 'utf-8');

  // 1. Front Matter validation
  const { error: fmErr, data: fm } = parseFrontMatter(content);
  if (fmErr) {
    errors.push(`[FrontMatter Error] ${fmErr}`);
  } else {
    if (!fm.type || !VALID_TYPES.includes(fm.type)) {
      errors.push(`[FrontMatter Error] Invalid or missing type: '${fm.type}'. Must be one of: ${VALID_TYPES.join(', ')}`);
    }
    if (!fm.domain) {
      errors.push(`[FrontMatter Error] Missing 'domain' field`);
    }
    if (!fm.name) {
      errors.push(`[FrontMatter Error] Missing 'name' field`);
    }
    if (!fm.status || !VALID_STATUSES.includes(fm.status)) {
      errors.push(`[FrontMatter Error] Invalid or missing status: '${fm.status}'. Must be one of: ${VALID_STATUSES.join(', ')}`);
    }
    if (isNaN(fm.confidence) || fm.confidence < 1 || fm.confidence > 5) {
      errors.push(`[FrontMatter Error] Invalid or missing confidence: '${fm.confidence}'. Must be integer 1-5`);
    }

    if (!fm.hasSourcesKey) {
      errors.push(`[FrontMatter Error] Missing 'sources' key`);
    } else if (fm.sourcesList.length === 0) {
      errors.push(`[FrontMatter Error] 'sources' list must not be empty`);
    } else {
      for (let i = 0; i < fm.sourcesList.length; i++) {
        const s = fm.sourcesList[i];
        if (!s.path) {
          errors.push(`[FrontMatter Error] Source item #${i + 1} missing required 'path'`);
        }
        if (!s.level || !VALID_EVIDENCE_LEVELS.includes(s.level)) {
          errors.push(`[FrontMatter Error] Source item #${i + 1} invalid or missing 'level': '${s.level}'. Must be one of: ${VALID_EVIDENCE_LEVELS.join(', ')}`);
        }
        if (!s.location) {
          errors.push(`[FrontMatter Error] Source item #${i + 1} missing required 'location'`);
        }
      }
    }

    if (!fm.last_verified || !/^\d{4}-\d{2}-\d{2}$/.test(fm.last_verified)) {
      errors.push(`[FrontMatter Error] Invalid or missing last_verified date: '${fm.last_verified}'. Expected format YYYY-MM-DD`);
    }
  }

  // 2. Link target validation
  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let linkMatch;
  while ((linkMatch = linkRegex.exec(content)) !== null) {
    const rawTarget = linkMatch[2];
    if (rawTarget.startsWith('http://') || rawTarget.startsWith('https://')) continue;
    if (rawTarget.startsWith('#')) continue;

    const targetPathNoHash = rawTarget.split('#')[0];
    if (!targetPathNoHash) continue;

    const absoluteTargetPath = path.resolve(path.dirname(filePath), targetPathNoHash);
    if (!fs.existsSync(absoluteTargetPath)) {
      errors.push(`[Link Error] Broken markdown link '${rawTarget}' -> target file not found: ${absoluteTargetPath}`);
    }
  }

  // 3. SQL safety & ROWNUM/LIMIT <= 20 validation (fenced code blocks + inline code / text)
  const sqlBlockRegex = /```sql([\s\S]*?)```/gi;
  let sqlMatch;
  while ((sqlMatch = sqlBlockRegex.exec(content)) !== null) {
    checkSqlStatement(sqlMatch[1], errors, 'fenced sql block');
  }

  // Inline backtick SQL statements (`SELECT ...`)
  const inlineSqlRegex = /`([^`]*\b(SELECT|WITH)\b[^`]*)`/gi;
  let inlineMatch;
  while ((inlineMatch = inlineSqlRegex.exec(content)) !== null) {
    checkSqlStatement(inlineMatch[1], errors, 'inline sql');
  }

  // 4. Required sections validation
  if (fm && fm.type) {
    if (fm.type === 'table') {
      const requiredHeadings = ['一句话定义', '数据粒度', '数据库约束', '核心字段', '脱敏样例', '关联'];
      for (const req of requiredHeadings) {
        if (!content.includes(req)) {
          errors.push(`[Card Section Error] Table card missing required section containing keyword '${req}'`);
        }
      }
    } else if (fm.type === 'metric') {
      const requiredHeadings = ['指标定义', '输出表', '公式'];
      for (const req of requiredHeadings) {
        if (!content.includes(req)) {
          errors.push(`[Card Section Error] Metric card missing required section containing keyword '${req}'`);
        }
      }
    } else if (fm.type === 'lineage') {
      const requiredHeadings = ['全景图', '逐段血缘'];
      for (const req of requiredHeadings) {
        if (!content.includes(req)) {
          errors.push(`[Card Section Error] Lineage card missing required section containing keyword '${req}'`);
        }
      }
    } else if (fm.type === 'rule') {
      if (!content.includes('规则标准文本描述')) {
        errors.push(`[Card Section Error] Rule card missing required section '规则标准文本描述'`);
      }
    } else if (fm.type === 'learning') {
      if (!content.includes('我真正需要记住的内容')) {
        errors.push(`[Card Section Error] Learning card missing required section '我真正需要记住的内容'`);
      }
      if (!content.includes('待确认问题')) {
        errors.push(`[Card Section Error] Learning card missing required section '待确认问题'`);
      }
    }
  }

  return { relativePath, errors };
}

function runValidation() {
  console.log('🔍 Starting Database Knowledge Base Validation Check...');
  console.log(`Target directory: ${dbKnowledgeDir}\n`);

  if (!fs.existsSync(dbKnowledgeDir)) {
    console.error(`❌ Error: ${dbKnowledgeDir} directory does not exist!`);
    process.exit(1);
  }

  const files = getAllMdFiles(dbKnowledgeDir);
  console.log(`Found ${files.length} Markdown knowledge files.`);

  let totalErrors = 0;
  const results = [];

  for (const file of files) {
    const res = validateFile(file);
    results.push(res);
    if (res.errors.length > 0) {
      totalErrors += res.errors.length;
    }
  }

  for (const res of results) {
    if (res.errors.length > 0) {
      console.log(`\n❌ ${res.relativePath}:`);
      for (const err of res.errors) {
        console.log(`   - ${err}`);
      }
    }
  }

  if (totalErrors === 0) {
    console.log(`\n✅ All ${files.length} database knowledge cards passed validation check successfully!`);
    process.exit(0);
  } else {
    console.error(`\n❌ Validation failed with ${totalErrors} errors across database knowledge files.`);
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  runValidation();
}
