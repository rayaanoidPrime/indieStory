import React, { useState } from "react";
import VideoPlayer from "./VideoPlayer";

const VideoGenerator = () => {
  const [prompt, setPrompt] = useState("");
  const [numImages, setNumImages] = useState(4);
  const [videoPath, setVideoPath] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    setVideoPath("");

    try {
      const response = await fetch(`${API_BASE_URL}/generate-video`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt, numImages }),
      });

      const data = await response.json();

      if (data.success) {
        setVideoPath(data.video_path);
      } else {
        setError("Failed to generate video");
      }
    } catch (err) {
      setError("An error occurred while generating the video");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt"
          required
        />
        <input
          type="number"
          value={numImages}
          onChange={(e) => setNumImages(parseInt(e.target.value))}
          min="1"
          max="10"
          required
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Generating..." : "Generate Video"}
        </button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {videoPath && <VideoPlayer videoPath={videoPath} />}
    </div>
  );
};

export default VideoGenerator;
