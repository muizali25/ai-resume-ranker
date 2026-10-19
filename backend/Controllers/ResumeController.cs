using AiResumeRanker.Models;
using AiResumeRanker.Services;
using Microsoft.AspNetCore.Mvc;

namespace AiResumeRanker.Controllers;

[ApiController]
[Route("api")]
public class ResumeController : ControllerBase
{
    private readonly GeminiService _gemini;
    private readonly IConfiguration _config;
    private readonly string _uploadsPath;
    private readonly int _maxResumes;

    public ResumeController(GeminiService gemini, IConfiguration config, IWebHostEnvironment env)
    {
        _gemini = gemini;
        _config = config;
        _maxResumes = config.GetValue("ResumeSettings:MaxResumes", 3);
        var folder = config["ResumeSettings:UploadsFolder"] ?? "uploads";
        _uploadsPath = Path.Combine(env.ContentRootPath, folder);

        if (!Directory.Exists(_uploadsPath))
        {
            Directory.CreateDirectory(_uploadsPath);
        }
    }

    private List<ResumeInfo> ListUploadedResumes()
    {
        if (!Directory.Exists(_uploadsPath))
            return new List<ResumeInfo>();

        var allowed = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            ".pdf", ".txt", ".md"
        };

        return Directory.GetFiles(_uploadsPath)
            .Where(fullPath => allowed.Contains(Path.GetExtension(fullPath)))
            .Select(fullPath =>
            {
                var savedName = Path.GetFileName(fullPath);
                var originalName = System.Text.RegularExpressions.Regex.Replace(
                    savedName, @"^\d+-", "");
                var info = new FileInfo(fullPath);
                return new ResumeInfo
                {
                    SavedName = savedName,
                    OriginalName = originalName,
                    Path = fullPath,
                    Size = info.Length
                };
            })
            .ToList();
    }

    // API 1: Upload resume (max 3)
    [HttpPost("upload")]
    public async Task<IActionResult> UploadResume(IFormFile resume)
    {
        var current = ListUploadedResumes();
        if (current.Count >= _maxResumes)
        {
            return BadRequest(new { error = $"Maximum {_maxResumes} resumes allowed. Delete some first." });
        }

        if (resume == null || resume.Length == 0)
        {
            return BadRequest(new { error = "No file uploaded" });
        }

        var ext = Path.GetExtension(resume.FileName).ToLowerInvariant();
        if (ext is not (".pdf" or ".txt" or ".md"))
        {
            return BadRequest(new { error = "Only PDF and TXT files are allowed" });
        }

        var safeName = System.Text.RegularExpressions.Regex.Replace(
            resume.FileName, @"[^a-zA-Z0-9._-]", "_");
        var savedName = $"{DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()}-{safeName}";
        var savePath = Path.Combine(_uploadsPath, savedName);

        await using (var stream = System.IO.File.Create(savePath))
        {
            await resume.CopyToAsync(stream);
        }

        var files = ListUploadedResumes();
        return Ok(new
        {
            message = "Resume uploaded",
            file = new
            {
                originalName = resume.FileName,
                savedName,
                size = resume.Length
            },
            resumes = files.Select(f => new
            {
                originalName = f.OriginalName,
                savedName = f.SavedName,
                size = f.Size
            })
        });
    }

    [HttpGet("resumes")]
    public IActionResult GetResumes()
    {
        var files = ListUploadedResumes();
        return Ok(new
        {
            resumes = files.Select(f => new
            {
                originalName = f.OriginalName,
                savedName = f.SavedName,
                size = f.Size
            }),
            count = files.Count,
            max = _maxResumes
        });
    }

    [HttpDelete("resumes/{savedName}")]
    public IActionResult DeleteResume(string savedName)
    {
        var filePath = Path.Combine(_uploadsPath, savedName);
        if (!System.IO.File.Exists(filePath))
        {
            return NotFound(new { error = "File not found" });
        }

        System.IO.File.Delete(filePath);
        var files = ListUploadedResumes();
        return Ok(new
        {
            message = "Resume deleted",
            resumes = files.Select(f => new
            {
                originalName = f.OriginalName,
                savedName = f.SavedName,
                size = f.Size
            })
        });
    }

    // API 2: Rank resumes with job description via Gemini
    [HttpPost("rank")]
    public async Task<IActionResult> RankWithJobDescription([FromBody] RankRequest request)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(request.JobDescription))
            {
                return BadRequest(new { error = "Job description is required" });
            }

            var files = ListUploadedResumes();
            if (files.Count == 0)
            {
                return BadRequest(new { error = "Upload at least one resume first" });
            }

            var bestMatch = await _gemini.RankResumesAsync(request.JobDescription, files);

            return Ok(new
            {
                bestMatch,
                message = $"Highly matched resume: {bestMatch}"
            });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new
            {
                error = "Failed to rank resumes",
                details = ex.Message
            });
        }
    }
}
