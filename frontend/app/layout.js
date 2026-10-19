import "./globals.css";

export const metadata = {
  title: "AI Resume Ranker",
  description: "Match resumes with job requirements using Google Gemini",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
