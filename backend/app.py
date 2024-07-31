from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.indie_story import IndieStory
from config import IndieStoryConfig

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class VideoRequest(BaseModel):
    prompt: str
    numImages: int = 4

@app.post("/generate-video")
async def generate_video(request: VideoRequest):
    writer_prompt = request.prompt
    num_images = request.numImages
    output_dir = 'output'

    config = IndieStoryConfig()
    indie_story = IndieStory(config)
    
    try:
        indie_story.generate(
            writer_prompt=writer_prompt,
            painter_prompt_prefix='',
            num_images=num_images,
            output_dir=output_dir
        )
        return {"success": True, "video_path": f"{output_dir}/out.mp4"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)