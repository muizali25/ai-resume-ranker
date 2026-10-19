# AI Resume Ranker

Upload up to **3 resumes**, paste a **job description**, and let **Google Gemini** pick the best matching resume.

Simple stack: **.NET 9 Web API** backend + **Next.js** frontend. No authentication. No heavy architecture.

---

## Features

- Upload resumes (PDF / TXT) — maximum **3**
- View uploaded resumes (name, size, remove)
- Paste job requirements in a multiline text box
- **Ask from AI** — Gemini compares resumes to the job description
- Displays the **highly matched resume name** only

---

## Tech Stack

| Layer    | Technology                                      |
|----------|-------------------------------------------------|
| Frontend | Next.js 14 (React)                              |
| Backend  | ASP.NET Core 9 Web API (Visual Studio 2022)     |
| AI       | Google Gemini (`gemini-1.5-flash`)              |
| PDF text | UglyToad.PdfPig                                 |

---

## Project Structure

```
ai-resume-ranker/
├── backend/                          # .NET 9 Web API
│   ├── AiResumeRanker.sln            # Open this in Visual Studio 2022
│   ├── AiResumeRanker.csproj
│   ├── Program.cs
│   ├── appsettings.json              # Gemini API key lives here
│   ├── Controllers/ResumeController.cs
│   ├── Services/GeminiService.cs     # Read / scan / prompt / call Gemini
│   ├── Models/
│   ├── uploads/                      # Saved resumes (sample PDFs included)
│   └── scripts/generate_sample_resumes.py
└── frontend/                         # Next.js UI (4 sections)
    └── app/page.js
```

---

## Prerequisites

- [.NET 9 SDK](https://dotnet.microsoft.com/download/dotnet/9.0)
- [Visual Studio 2022](https://visualstudio.microsoft.com/) (optional, recommended)
- [Node.js](https://nodejs.org/) 18+
- A [Google Gemini API key](https://aistudio.google.com/apikey)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-ranker.git
cd ai-resume-ranker
```

### 2. Backend

1. Open `backend/AiResumeRanker.sln` in **Visual Studio 2022**, **or** use the terminal.
2. Add your Gemini API key in `backend/appsettings.json`:

```json
"Gemini": {
  "ApiKey": "YOUR_GEMINI_API_KEY_HERE",
  "Model": "gemini-1.5-flash"
}
```

3. Run the API:

**Visual Studio:** press **F5**

**Terminal:**

```bash
cd backend
dotnet restore
dotnet run
```

Backend URL: **http://localhost:5000**

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000**

---

## How to Use

1. Open the UI at `http://localhost:3000`
2. Upload up to 3 resumes (or use the sample PDFs already in `backend/uploads`)
3. Paste the job description
4. Click **Ask from AI**
5. See the best matching resume name in section 4

### Sample resumes included

Three 5-page sample PDFs are already in `backend/uploads` so the UI can show them immediately:

| File | Role |
|------|------|
| `Software_Engineer_Alex_Rivera.pdf` | Software Engineer |
| `Mechanical_Engineer_Jordan_Blake.pdf` | Mechanical Engineer |
| `Electrical_Engineer_Samira_Khan.pdf` | Electrical Engineer |

Each includes intro, summary, contact, education, skills, projects, experience, and hobbies.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/upload` | Upload a resume (`multipart/form-data`, field: `resume`) |
| `GET` | `/api/resumes` | List uploaded resumes |
| `DELETE` | `/api/resumes/{savedName}` | Delete a resume |
| `POST` | `/api/rank` | Rank resumes — body: `{ "jobDescription": "..." }` |

### Example rank request

```http
POST http://localhost:5000/api/rank
Content-Type: application/json

{
  "jobDescription": "We need a software engineer with React, Node.js, and cloud experience."
}
```

### Example response

```json
{
  "bestMatch": "Software_Engineer_Alex_Rivera.pdf",
  "message": "Highly matched resume: Software_Engineer_Alex_Rivera.pdf"
}
```

---

## Backend Notes

- One controller: `ResumeController`
- Gemini helpers in `GeminiService`: `ReadFile`, `ScanDocument`, `MakePrompt`, `CallGeminiAsync`, `RankResumesAsync`
- API key is read from `appsettings.json` (not hardcoded in service logic)
- CORS enabled for local frontend
- No authentication

---

## License

See [LICENSE](LICENSE) for details.
