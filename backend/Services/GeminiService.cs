using System.Text;
using System.Text.Json;
using AiResumeRanker.Models;
using UglyToad.PdfPig;

namespace AiResumeRanker.Services;

public class GeminiService
{
    private readonly string _apiKey;
    private readonly string _model;
    private readonly HttpClient _http;

    public GeminiService(IConfiguration config, IHttpClientFactory httpClientFactory)
    {
        _apiKey = config["Gemini:ApiKey"] ?? "";
        _model = config["Gemini:Model"] ?? "gemini-1.5-flash";
        _http = httpClientFactory.CreateClient();
    }

    // Read raw file bytes from disk
    public byte[] ReadFile(string filePath)
    {
        return File.ReadAllBytes(filePath);
    }

    // Extract text from PDF or plain text resume
    public string ScanDocument(string filePath)
    {
        var ext = Path.GetExtension(filePath).ToLowerInvariant();

        if (ext == ".pdf")
        {
            var sb = new StringBuilder();
            using var document = PdfDocument.Open(filePath);
            foreach (var page in document.GetPages())
            {
                sb.AppendLine(page.Text);
            }
            return sb.ToString();
        }

        if (ext is ".txt" or ".md")
        {
            return File.ReadAllText(filePath);
        }

        return File.ReadAllText(filePath);
    }

    // Build the prompt for Gemini
    public string MakePrompt(string jobDescription, List<(string Name, string Text)> resumes)
    {
        var resumeBlock = new StringBuilder();
        for (var i = 0; i < resumes.Count; i++)
        {
            resumeBlock.AppendLine($"\n--- Resume {i + 1}: {resumes[i].Name} ---");
            resumeBlock.AppendLine(resumes[i].Text);
        }

        return $"""
            You are a hiring assistant. Compare the resumes below with the job description.
            Return ONLY the file name of the single best matching resume. No extra text, no explanation.

            Job Description:
            {jobDescription}

            Resumes:
            {resumeBlock}

            Best matching resume file name:
            """;
    }

    // Call Google Gemini and get response text
    public async Task<string> CallGeminiAsync(string prompt)
    {
        var url =
            $"https://generativelanguage.googleapis.com/v1beta/models/{_model}:generateContent?key={_apiKey}";

        var body = new
        {
            contents = new[]
            {
                new
                {
                    parts = new[]
                    {
                        new { text = prompt }
                    }
                }
            }
        };

        var json = JsonSerializer.Serialize(body);
        using var content = new StringContent(json, Encoding.UTF8, "application/json");
        using var response = await _http.PostAsync(url, content);
        var responseText = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Gemini API error: {response.StatusCode} - {responseText}");
        }

        using var doc = JsonDocument.Parse(responseText);
        var text = doc.RootElement
            .GetProperty("candidates")[0]
            .GetProperty("content")
            .GetProperty("parts")[0]
            .GetProperty("text")
            .GetString();

        return (text ?? "").Trim();
    }

    // Main: rank resumes against job description, return best name
    public async Task<string> RankResumesAsync(string jobDescription, List<ResumeInfo> uploadedFiles)
    {
        var resumes = new List<(string Name, string Text)>();

        foreach (var file in uploadedFiles)
        {
            var text = ScanDocument(file.Path);
            resumes.Add((file.OriginalName, text));
        }

        var prompt = MakePrompt(jobDescription, resumes);
        var answer = await CallGeminiAsync(prompt);

        var match = uploadedFiles.FirstOrDefault(f =>
            answer.Contains(f.OriginalName, StringComparison.OrdinalIgnoreCase));

        return match?.OriginalName ?? answer;
    }
}
