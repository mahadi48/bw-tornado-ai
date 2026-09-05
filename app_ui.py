import os
import requests
import streamlit as st

# 페이지 কনফিগারেশন (Page Configuration)
st.set_page_config(
    page_title="BW Tornado AI Video Studio",
    page_icon="🌪️",
    layout="wide",
)

# ব্যাকএন্ড ইউআরএল সেটআপ (আপনার রেন্ডার লিংক এখানে সেট করা আছে)
BACKEND_URL = os.getenv("BACKEND_URL", "https://bw-tornado-ai.onrender.com")

st.title("🌪️ BW Tornado AI Video Studio")
st.write(
    "Welcome to the AI video studio! Upload your large files (up to 2GB) and"
    " process them seamlessly."
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
        # ফাইলটি ব্যাকএন্ডে পাঠানোর প্রস্তুতি
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }

        # Render ব্যাকএন্ডে রিকোয়েস্ট পাঠানো
        response = requests.post(f"{BACKEND_URL}/process-video/", files=files)

        if response.status_code == 200:
          st.success("Video processed successfully!")
          result_data = response.json()
          st.json(result_data)
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
