---
description: Generate a PR summary from the current branch's changes
allowed-tools: Read, Bash, Grep, Glob
argument-hint: "[base-branch]"
---

# PR Summary Generator

Generate a well-structured pull request summary for the current branch.

## Context

Branch info:
!`git branch --show-current`

Commits on this branch (compared to main):
!`git log --oneline main..HEAD 2>/dev/null || git log --oneline origin/main..HEAD 2>/dev/null || echo "No commits found relative to main"`

Files changed:
!`git diff --stat main..HEAD 2>/dev/null || git diff --stat origin/main..HEAD 2>/dev/null || echo "No diff found relative to main"`

Full diff:
!`git diff main..HEAD 2>/dev/null || git diff origin/main..HEAD 2>/dev/null || echo "No diff found"`

## Instructions

Based on the above context, generate a PR summary with the following structure:

```markdown
## Summary
<!-- 1-3 sentences describing what this PR does and why -->

## Changes
<!-- Bulleted list of specific changes, grouped by category -->

### Added
- ...

### Changed
- ...

### Fixed
- ...

## Testing
<!-- How to test these changes -->
- [ ] ...

## Notes
<!-- Any additional context, migration steps, or things reviewers should know -->
```

Guidelines:
- Focus on the "why" — not just listing what changed
- Group related changes together
- Mention any breaking changes prominently
- Include migration steps if database or config changes are involved
- Keep it concise — reviewers are busy
