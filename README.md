# AI Resume Ranker

Simple app: upload up to 3 resumes, paste a job description, and Google Gemini picks the best match.

## Structure

```
backend/     .NET 9 Web API + Gemini service (Visual Studio 2022)
frontend/    Next.js UI (4 sections)
```

## Setup

### 1. Backend (.NET 9)

Open **`backend/AiResumeRanker.sln`** in **Visual Studio 2022**.

Set your Gemini API key in `backend/appsettings.json`:

```json
"Gemini": {
  "ApiKey": "YOUR_GEMINI_API_KEY_HERE",
  "Model": "gemini-1.5-flash"
}
```

**Visual Studio:** press **F5** (or green Run).

**Terminal:**

```bash
cd backend
dotnet run
```

API: `http://localhost:5000`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`

## APIs

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/upload` | Upload resume (form field: `resume`) |
| GET | `/api/resumes` | List uploaded resumes |
| DELETE | `/api/resumes/{savedName}` | Remove a resume |
| POST | `/api/rank` | Body: `{ "jobDescription": "..." }` → best match name |

## Notes

- Max 3 resumes
- Supported files: PDF, TXT
- No authentication
- Gemini helpers: `ReadFile`, `ScanDocument`, `MakePrompt`, `CallGeminiAsync`, `RankResumesAsync`
