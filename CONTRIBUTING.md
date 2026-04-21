# Contributing to Cortex

Thank you for your interest in contributing to Cortex! This document provides guidelines and instructions for contributing.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guide](#style-guide)
- [Commit Messages](#commit-messages)

---

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct:

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive criticism
- Resolve conflicts professionally

---

## Getting Started

### Prerequisites

- Git
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional but recommended)
- PostgreSQL 12+ (if running locally)

### Fork & Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cortex.git
   cd cortex
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/cortex/cortex.git
   ```

---

## Development Setup

### Using Docker (Recommended)

```bash
# Start development environment
docker-compose up -d

# Access services
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

---

## Making Changes

### Create a Feature Branch

```bash
# Update main
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `perf/` - Performance improvements
- `test/` - Test additions/improvements

### Development Workflow

1. **Make your changes**
   - Write clean, well-documented code
   - Follow the style guide
   - Add tests for new functionality

2. **Test your changes**
   ```bash
   # Backend
   cd cortex/backend
   pytest
   black .
   flake8 .
   mypy .
   
   # Frontend
   cd cortex/frontend
   pnpm test
   pnpm lint
   ```

3. **Commit frequently**
   - Write clear commit messages
   - Reference issues when applicable

4. **Keep branch updated**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

---

## Testing

### Backend Tests

```bash
cd cortex/backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_chat.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Frontend Tests

```bash
cd cortex/frontend

# Run tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run with coverage
pnpm test:coverage
```

### Manual Testing

1. Start services: `docker-compose up -d`
2. Open http://localhost:5173
3. Test features thoroughly:
   - Chat functionality
   - Memory operations
   - Dream cycles
   - Tool execution
   - Discord integration
   - Tailscale networking

### Code Quality

```bash
# Backend code quality
cd cortex/backend
black .              # Format code
isort .              # Sort imports
flake8 .             # Lint
mypy .               # Type checking

# Frontend code quality
cd cortex/frontend
pnpm lint            # Lint code
pnpm format          # Format code
```

---

## Submitting Changes

### Prepare Your Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**:
   - Go to GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out PR template

### Pull Request Template

```markdown
## Description
Briefly describe your changes and why you're making them.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
Describe testing performed:
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] No tests needed

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] All tests pass
- [ ] Commit messages are clear

## Screenshots (if applicable)
Add screenshots for UI changes
```

### PR Review Process

1. **Automated Checks**
   - CI/CD pipeline runs
   - Code quality checks
   - Test suite execution

2. **Code Review**
   - Maintainers review your code
   - Provide feedback if needed
   - Request changes if necessary

3. **Approval & Merge**
   - After approval, maintainers merge
   - Celebrate your contribution! 🎉

---

## Style Guide

### Backend (Python)

**Follow PEP 8** with these specifics:

```python
# Imports: standard, third-party, local
import os
from typing import Optional, List

import aiohttp
import sqlalchemy

from app.models import User
from app.services import memory_service

# Type hints for all functions
async def process_message(
    message: str,
    context: Dict[str, Any],
) -> Dict[str, Any]:
    """Process a message through the agent.
    
    Args:
        message: The message to process
        context: Contextual information
        
    Returns:
        Dictionary with response and metadata
    """
    pass

# Docstrings for all public functions
class CortexAgent:
    """Main Cortex AI agent.
    
    Handles chat, memory, and tool execution.
    """
    pass
```

### Frontend (TypeScript/Svelte)

**Follow Svelte/TypeScript best practices**:

```typescript
// Imports organized: svelte, third-party, local
import { onMount } from 'svelte';
import { derived } from 'svelte/store';
import type { User } from '$lib/types';

import { apiClient } from '$lib/api/client';
import MemoryCard from './MemoryCard.svelte';

// Type all props and state
interface Props {
  userId: string;
  initialMemories: Memory[];
  onMemoryClick?: (id: string) => void;
}

let { userId, initialMemories = [], onMemoryClick }: Props = $props();

// JSDoc for component functions
/**
 * Fetch and load memories for the user
 */
async function loadMemories(): Promise<void> {
  // implementation
}
```

### File Structure

**Backend**:
```python
# descriptive_name.py
# - Imports at top
# - Type hints throughout
# - Docstrings for modules, classes, functions
# - Constants in UPPER_CASE
# - Private functions start with _
```

**Frontend**:
```svelte
<!-- DescriptiveComponent.svelte -->
<script lang="ts">
  // Imports, props, stores
  // Logic (functions, handlers)
</script>

<!-- HTML structure -->

<style>
  /* Component scoped styles */
</style>
```

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructure
- `perf`: Performance improvement
- `test`: Test changes
- `chore`: Build/dependencies

### Scope

Component/module affected: `chat`, `memory`, `discord`, `api`, etc.

### Subject

- Imperative mood ("add" not "adds")
- No period at end
- Less than 50 characters

### Body

- Explain what and why (not how)
- Wrap at 72 characters
- Separate from subject with blank line

### Footer

- Reference issues: `Fixes #123`
- Breaking changes: `BREAKING CHANGE: ...`

### Examples

```
feat(memory): add semantic search to memory store

Implement vector-based search for memory retrieval,
allowing better contextual matching of memories.

Fixes #456
```

```
fix(discord): handle message length limits

Discord has a 2000 character limit per message.
Implement message splitting for long responses.

Closes #789
```

---

## Additional Resources

### Documentation
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Development setup
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview

### External Resources
- [Python Style Guide](https://pep8.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Svelte Documentation](https://svelte.dev/docs)
- [FastAPI Guide](https://fastapi.tiangolo.com/)

### Getting Help

- **Questions**: Create a GitHub Discussion
- **Issues**: Report bugs with detailed information
- **Chat**: Join our community chat (link)

---

## Areas for Contribution

### High Priority

- [ ] Improve test coverage (targeting 80%+)
- [ ] Add performance optimizations
- [ ] Enhance error handling
- [ ] Improve documentation

### Medium Priority

- [ ] Add new tool integrations
- [ ] Improve UI/UX
- [ ] Add more API endpoints
- [ ] Implement caching

### Community

- [ ] Bug reports
- [ ] Feature requests
- [ ] Documentation improvements
- [ ] Translation contributions

---

## Recognition

Contributors are recognized in:

- [CONTRIBUTORS.md](CONTRIBUTORS.md) - Contributor list
- Release notes
- Project documentation

---

## Questions?

- Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- Review existing issues/PRs
- Create a GitHub Discussion
- Contact maintainers

---

## License

By contributing, you agree that your contributions will be licensed under the same MIT License as the project.

---

**Thank you for contributing to Cortex! 🚀**
