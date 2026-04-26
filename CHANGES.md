# CHANGES.md

This file tracks all changes made by Claude Code in this repository.

---

## 2026-04-26

### Docker build fixes

**`frontend/Dockerfile`**

- Fixed wrong build output path in runtime stage: `.svelte-kit/build` → `build` (`adapter-static` outputs to `build/`, not `.svelte-kit/build/`)
- Added `ARG`/`ENV` for `VITE_API_URL` and `VITE_WS_URL` so they are baked into the static bundle at build time

**`Dockerfile.frontend`** (root / used by CI)

- Rewrote as a proper multi-stage build (was single-stage with no runtime separation)
- Added `COPY frontend/static ./static` — static assets (fonts, icons, etc.) were not being copied before `npm run build`
- Added `ARG`/`ENV` for `VITE_API_URL` and `VITE_WS_URL`
- Fixed port mismatch: `EXPOSE 3000` + `npm run preview` → `EXPOSE 5173` + `serve -s build -l 5173`
- Added healthcheck

**`Dockerfile.backend`** (root / used by CI)

- Fixed non-root user permission bug: `pip install --user` wrote packages to `/root/.local`, which is inside `/root` (mode `700`) and inaccessible to the `cortex` user the container runs as. Changed to install without `--user` and copy from `/usr/local/lib/python3.11/site-packages/` instead.

**`docker-compose.yml`**

- Frontend: replaced runtime `environment:` block for `VITE_*` vars with `build.args:` — these vars are baked at build time by Vite and have no effect at runtime
- Backend healthcheck: `/docs` → `/health` (Swagger docs may be disabled in production)

**`backend/Dockerfile`**

- Healthcheck: `/docs` → `/health`

**`Makefile`**

- Fixed `lint` target: `cd backend && pylint backend/` → `cd backend && pylint . --ignore=.venv,migrations` (was trying to lint a non-existent subdirectory)

**`.dockerignore` files** (all new)

- `.dockerignore` (root): excludes `**/node_modules`, `**/.venv`, `**/__pycache__`, etc. for CI builds
- `frontend/.dockerignore`: excludes `node_modules`, `.svelte-kit`, `build`
- `backend/.dockerignore`: excludes `.venv`, `__pycache__`, `*.pyc`, etc.

### Documentation

- Created `CLAUDE.md` — guidance file for Claude Code instances working in this repo
- Created `CHANGES.md` — this file

---

### Documentation fixes

**`QUICK_START.md`** (major corrections — file referenced a different project layout)

- Removed "100% complete / Production Ready" status claim (contradicted README)
- Removed hardcoded absolute path `/home/aster/Documents/Cortex-Project`
- Fixed all `cortex/backend` → `backend`, `cortex/frontend` → `frontend` path references
- Fixed backend startup command: `python -m uvicorn app.main:app --reload` → `uvicorn main:app --reload`
- Fixed frontend package manager: `pnpm install` / `pnpm dev` → `npm install` / `npm run dev`
- Fixed CLI paths: `cortex/cli/cortex_cli.py` → `cli/cortex_cli.py`
- Fixed frontend config path: `cortex/frontend/.env.local` → `frontend/.env`
- Fixed "Adding New Features" paths: `app/routes/`, `app/main.py`, `app/models/` → correct `backend/` paths
- Fixed test command: `cd cortex/backend && pytest` → `cd backend && pytest test -v`
- Fixed project structure tree to match actual repo layout
- Added stub warnings for Discord and Tailscale sections

**`README.md`**

- Fixed frontend URL in Docker Compose section: `http://localhost:3000` → `http://localhost:5173`
- Fixed test command: `pytest backend/test -v` (run from inside `backend/`) → `pytest test -v`
- Fixed lint command: `flake8 backend` (non-existent subdir) → `flake8 .`
