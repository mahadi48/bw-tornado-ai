import os
import requests
import streamlit as st

# পেজ কনফিগারেশন এবং ডার্ক থিম সেটআপ
st.set_page_config(
    page_title="BW Tornado AI Video Studio",
    page_icon="🌪️",
    layout="wide",
)

# ব্যাকএন্ড ইউআরএল সেটআপ (Render-এর লাইভ লিংক)
BACKEND_URL = os.getenv("BACKEND_URL", "https://bw-tornado-ai.onrender.com")

# সাইডবারে লোগো, ব্র্যান্ড নেম, মুড, ক্যাটেগরি ও ডেসক্রিপশন অপশন
with st.sidebar:
  # আপনার লোগো এবং ব্র্যান্ড নেম সেকশন
  st.markdown("<h1 style='text-align: center;'>🌪️</h1>", unsafe_allow_html=True)
  st.markdown(
      "<h2 style='text-align: center; color: #ff4b4b;'>BW Tornado</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: gray;'>AI Video Studio</p>",
      unsafe_allow_html=True,
  )
  st.markdown("---")

  st.markdown("### ⚙️ Video Settings")
  category = st.selectbox(
      "Select Category",
      [
          "Gaming (Free Fire/PUBG)",
          "Vlog",
          "Shorts/Reels",
          "Tutorial",
          "Cinematic",
      ],
  )
  mood = st.selectbox(
      "Select Mood",
      [
          "Funny & Energetic",
          "Serious & Professional",
          "Hype & Action",
          "Sad/Emotional",
      ],
  )
  description = st.text_area(
      "Description / Custom Prompt",
      placeholder=(
          "e.g., Remove boring parts, make it funny, increase volume..."
      ),
  )

  st.markdown("---")
  st.info("Status: Connected to Render Backend")

# মূল পেজের হেডিং
st.title("🌪️ BW Tornado AI Video Studio")
st.markdown(
    "Welcome to your professional AI video studio. Configure your settings in"
    " the sidebar, upload your video, and process it seamlessly."
)

# ফাইল আপলোড অপশন (২ জিবি পর্যন্ত সাপোর্ট করবে)
uploaded_file = st.file_uploader(
    "Choose a video file", type=["mp4", "mov", "avi", "mkv"]
)

if uploaded_file is not None:
  st.video(uploaded_file)

  if st.button("Process Video"):
    with st.spinner("Processing video with AI backend..."):
      try:
        # ফাইল এবং অন্যান্য ডেটা ব্যাকএন্ডে পাঠানোর প্রস্তুতি
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }
        data = {"category": category, "mood": mood, "description": description}

        # Render ব্যাকএন্ডে রিকোয়েস্ট পাঠানো (লোকাল হোস্টের পরিবর্তে লাইভ লিংক)
        response = requests.post(
            f"{BACKEND_URL}/process-video/", files=files, data=data
        )

        if response.status_code == 200:
          st.success("Video processed successfully!")
          result_data = response.json()
          st.json(result_data)

          # ডাউনলোড সেকশন
          st.markdown("### 📥 Download Processed Video")
          st.download_button(
              label="Download Final Video",
              data=uploaded_file.getvalue(),
              file_name=f"processed_{uploaded_file.name}",
              mime=uploaded_file.type,
          )
        else:
          st.error(
              f"Server error: Received status code {response.status_code}"
          )

      except requests.exceptions.ConnectionError:
        st.error(
            f"সারভারের সাথে সংযোগ স্থাপন করা যায়নি: ব্যাকএন্ড সার্ভার ({BACKEND_URL})"
            " চালু আছে কি না চেক করুন।"
        )
      except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# নিচে ব্যবহারের নিয়ম বা গাইডলাইন সেকশন
st.markdown("---")
st.markdown("### 📌 ব্যবহারের নিয়মাবলী (Instructions & Guidelines):")
st.markdown(
    """
1. **সর্বোচ্চ ফাইল সাইজ:** আপনি সর্বোচ্চ **2GB** পর্যন্ত ভিডিও ফাইল আপলোড করতে পারবেন।
2. **সাপোর্টেড ফরম্যাট:** শুধুমাত্র MP4, MOV, AVI, এবং MKV ফরম্যাটের ভিডিও ফাইলগুলো আপলোড করুন।
3. **কাস্টমাইজেশন:** সাইডবার থেকে আপনার পছন্দের **Category**, **Mood** এবং **Description** সেট করে নিন।
4. **ডাউনলোড:** ভিডিও প্রসেসিং শেষ হওয়ার পর নিচের **Download** বাটন থেকে ফাইনাল ফাইলটি নামিয়ে নিন।
"""
)
