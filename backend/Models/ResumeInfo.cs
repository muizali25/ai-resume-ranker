namespace AiResumeRanker.Models;

public class ResumeInfo
{
    public string OriginalName { get; set; } = "";
    public string SavedName { get; set; } = "";
    public long Size { get; set; }
    public string Path { get; set; } = "";
}

public class RankRequest
{
    public string JobDescription { get; set; } = "";
}
