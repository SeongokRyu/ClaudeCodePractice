# Project: Production Multi-Agent Pipeline

This project demonstrates a production-ready multi-agent pipeline using Claude Code's Command → Agent → Skill architecture.

## Architecture
- **Commands**: `/build-feature` orchestrates the full pipeline
- **Agents**: researcher, implementer, reviewer (with memory), tester
- **Skills**: coding-conventions, testing-patterns, security-review

## Code Conventions
- Python with type hints throughout
- Dataclasses for structured data
- Docstrings on all public APIs
- Error handling with descriptive messages
- Functions under 30 lines

## Testing
- Test files: `test_*.py` next to source files
- Framework: pytest
- Pattern: pytest classes and functions
- Coverage target: 80%+

## File Structure
```
src/
├── app.py          — Main application module
├── test_app.py     — Tests for app module
└── [new_module].py — New modules added by the pipeline
```
