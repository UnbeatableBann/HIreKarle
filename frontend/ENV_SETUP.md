# Frontend Environment Setup

## Environment File Created

✅ `.env` - Active environment file
✅ `.env.example` - Template file

## Configuration

**File:** `frontend/.env`

```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Usage

The API service automatically uses this environment variable:

```javascript
// api.js
const API_BASE_URL = `${process.env.REACT_APP_API_BASE_URL}/api`;
```

## Change Backend URL

To connect to a different backend:

1. Edit `frontend/.env`
2. Change `REACT_APP_API_BASE_URL` value
3. Restart frontend: `npm start`

### Examples

**Local:**
```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

**Production:**
```env
REACT_APP_API_BASE_URL=https://api.yourdomain.com
```

**Different Port:**
```env
REACT_APP_API_BASE_URL=http://localhost:8001
```

## Important Notes

- ⚠️ Must start with `REACT_APP_` (React requirement)
- ⚠️ Restart frontend after changing `.env`
- ⚠️ Don't commit `.env` to git (already in .gitignore)
- ✅ Commit `.env.example` as template

## Setup for New Users

```bash
cd frontend
cp .env.example .env
# Edit .env if needed
npm install
npm start
```
