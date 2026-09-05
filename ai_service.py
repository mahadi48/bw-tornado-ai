from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import cv2
from moviepy import VideoFileClip
import os

app = FastAPI(title="AI Video Editor & Thumbnail Service - BW Tornado")

class VideoProcessRequest(BaseModel):
    video_filename: str
    output_video_name: str = "edited_output.mp4"
    thumbnail_name: str = "output_thumbnail.png"

@app.get("/")
def home():
    return {"message": "BW Tornado AI Video Editor & Thumbnail Service is running!"}

def process_heavy_video(video_path: str, output_name: str, thumb_name: str):
    """বড় ভিডিও ব্যাকগ্রাউন্ডে প্রসেস করার ফাংশন"""
    try:
        # MoviePy দিয়ে ভিডিও প্রসেসিং (বড় ভিডিওর জন্য ultrafast প্রিসেট)
        clip = VideoFileClip(video_path)
        clip.write_videofile(output_name, codec="libx264", audio_codec="aac", preset="ultrafast")
        clip.close()

        # OpenCV দিয়ে থাম্বনেইল তৈরি (৫ সেকেন্ডের ফ্রেম)
        vidcap = cv2.VideoCapture(video_path)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, int(fps * 5)) 
        success, image = vidcap.read()
        
        if success:
            cv2.imwrite(thumb_name, image)
        vidcap.release()
    except Exception as e:
        print(f"Background Processing Error: {e}")

@app.post("/process-video/")
def process_video(data: VideoProcessRequest, background_tasks: BackgroundTasks):
    try:
        # চেক করা ভিডিও ফাইলটি কম্পিউটারে আছে কি না
        if not os.path.exists(data.video_filename):
            raise HTTPException(status_code=404, detail="Video file not found in path!")

        # ব্যাকগ্রাউন্ড টাস্কে ভিডিও প্রসেসিং ছেড়ে দেওয়া (যাতে টাইম-আউট না হয়)
        background_tasks.add_task(
            process_heavy_video, 
            data.video_filename, 
            data.output_video_name, 
            data.thumbnail_name
        )

        return {
            "status": "processing",
            "message": "ভিডিও প্রসেসিং শুরু হয়েছে! ১ ঘণ্টার বড় ভিডিও হওয়ায় ব্যাকগ্রাউন্ডে কাজ চলতে থাকবে।",
            "edited_video": data.output_video_name,
            "thumbnail": data.thumbnail_name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))