#!/usr/bin/env node
// Cross-checks .claude-plugin/plugin.json's "skills" list against the SKILL.md
// files that actually exist on disk. Fails loudly instead of letting a skill
// silently drop out of the installable plugin.
//
// Checks:
//   1. Every skills/**/SKILL.md on disk is registered in plugin.json.
//   2. Every path registered in plugin.json points at a real SKILL.md.
//   3. Each SKILL.md's frontmatter `name:` matches its directory name.

import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, relative, basename } from "node:path";
import { fileURLToPath } from "node:url";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const skillsRoot = join(repo, "skills");
const pluginPath = join(repo, ".claude-plugin", "plugin.json");

function findSkillDirs(dir) {
  const found = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      found.push(...findSkillDirs(full));
    } else if (entry.isFile() && entry.name === "SKILL.md") {
      found.push(dir);
    }
  }
  return found;
}

function frontmatterName(skillMdPath) {
  const text = readFileSync(skillMdPath, "utf8");
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;
  const nameLine = match[1].split(/\r?\n/).find((l) => /^name:/.test(l));
  return nameLine ? nameLine.replace(/^name:\s*/, "").trim() : null;
}

const onDiskDirs = findSkillDirs(skillsRoot).map((d) =>
  "./" + relative(repo, d).replace(/\\/g, "/"),
);

const plugin = JSON.parse(readFileSync(pluginPath, "utf8"));
const registered = plugin.skills ?? [];

const errors = [];

for (const dir of onDiskDirs) {
  if (!registered.includes(dir)) {
    errors.push(`missing from plugin.json "skills": ${dir}`);
  }
}

for (const path of registered) {
  const absDir = join(repo, path);
  let hasSkillMd = false;
  try {
    hasSkillMd = statSync(join(absDir, "SKILL.md")).isFile();
  } catch {
    hasSkillMd = false;
  }
  if (!hasSkillMd) {
    errors.push(`plugin.json lists "${path}" but skills/SKILL.md was not found there`);
  }
}

for (const dir of onDiskDirs) {
  const skillMdPath = join(repo, dir, "SKILL.md");
  const name = frontmatterName(skillMdPath);
  const folderName = basename(dir);
  if (name && name !== folderName) {
    errors.push(
      `${dir}/SKILL.md frontmatter name "${name}" does not match folder name "${folderName}"`,
    );
  }
}

if (errors.length > 0) {
  console.error(`Found ${errors.length} problem(s):\n`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}

console.log(`All ${onDiskDirs.length} skills on disk match plugin.json registration.`);
