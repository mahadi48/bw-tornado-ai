import streamlit as st
import requests
import os

# পেজের লেআউট এবং টাইটেল সেট করা (Wide mode)
st.set_page_config(
    page_title="BW Tornado - AI Video & Thumbnail Hub",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# প্রফেশনাল গেমিং ও মডার্ন ডার্ক CSS স্টাইল
st.markdown("""
    <style>
    /* Main Dark Background */
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    
    /* Sidebar Dark Background */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
    }
    
    /* General text readability in dark mode */
    .stMarkdown, p, span, label, div {
        color: #ffffff;
    }
    
    /* Description Text Area Input Text Color Dark */
    textarea {
        color: #000000 !important;
    }
    
    /* File Uploader Text Color Dark */
    [data-testid="stFileUploader"] section {
        color: #000000 !important;
    }
    [data-testid="stFileUploader"] div, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small {
        color: #000000 !important;
    }
    
    .main-title {
        font-size: 32px;
        color: #00ffcc;
        text-align: center;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        color: #a0a0a0;
        text-align: center;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00ffcc 0%, #0077ff 100%);
        color: #0e1117;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        height: 55px;
        border: none;
        box-shadow: 0px 4px 15px rgba(0, 255, 204, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0077ff 0%, #00ffcc 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# লোগো ডিসপ্লে করার সেকশন
col_logo1, col_logo2, col_logo3 = st.columns([1, 1.5, 1])
with col_logo2:
    logo_path_jpg = "logo.jpg"
    logo_path_png = "logo.png"
    
    if os.path.exists(logo_path_jpg):
        st.image(logo_path_jpg, use_container_width=True)
    elif os.path.exists(logo_path_png):
        st.image(logo_path_png, use_container_width=True)
    else:
        st.warning("⚠️ লোগো পাওয়া যায়নি! ব্যাকএন্ড ফোল্ডারে logo.jpg বা logo.png নামে সেভ করুন।")

st.markdown('<div class="main-title">BW TORNADO AI STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Bengal Warriors - Next-Gen Video Editor & Thumbnail Hub</div>', unsafe_allow_html=True)

st.divider()

# সাইডবার ডিজাইন এবং নির্দেশাবলী
with st.sidebar:
    st.header("⚙️ কন্ট্রোল প্যানেল")
    st.markdown("---")
    st.markdown("🔥 **ব্র্যান্ড:** BW Tornado")
    st.markdown("⚡ **স্ট্যাটাস:** অনলাইন & রেডি")
    st.markdown("---")
    st.markdown("### 📜 অপশন গাইড:")
    st.markdown("- **Category:** ভিডিওর ধরন সিলেক্ট করুন।")
    st.markdown("- **Mood:** ভিডিওর ভাইব (Funny, Sad ইত্যাদি) সেট করুন।")
    st.markdown("- **Description:** আপনার নির্দেশনা লিখে দিন।")

# ১. ভিডিও ক্যাটাগরি সিলেক্ট করার অপশন
video_category = st.selectbox(
    "🎯 আপনার ভিডিওর ক্যাটাগরি সিলেক্ট করুন:",
    ("🎮 Gaming Highlights / Free Fire", "🎬 Vlogs & General Videos", "💻 Tech & Tutorial Videos")
)

# ২. ভিডিওর মুড বা ভাইব সিলেক্ট করার অপশন
video_mood = st.selectbox(
    "🎭 ভিডিওর মুড বা ভাইব (Mood) সিলেক্ট করুন:",
    ("🔥 Hype & Action-Packed", "😂 Funny & Entertaining", "😢 Sad & Emotional", "💼 Professional & Clean", "✨ Epic & Cinematic")
)

# ৩. ডেসক্রিপশন বা এআই ইনস্ট্রাকশন লেখার অপশন
video_description = st.text_area(
    "📝 এআই-এর জন্য আপনার নির্দেশনা (Description/Instructions):",
    placeholder="যেমন: ভিডিওর ফানি মোমেন্টগুলো ফোকাস করো..."
)

# ফাইল আপলোড সেকশন
uploaded_file = st.file_uploader("📁 আপনার ভিডিও ফাইল এখানে ড্রপ করুন (.mp4, .mov, .avi)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.success(f"সফলভাবে আপলোড হয়েছে! ক্যাটাগরি: {video_category} | মুড: {video_mood}")
    st.video(uploaded_file)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 প্রসেস শুরু করুন (Start AI Processing)"):
        with st.spinner("⚡ BW Tornado AI ভিডিও এডিট এবং থাম্বনেইল তৈরি করছে... একটু অপেক্ষা করুন..."):
            # ভিডিও ফাইলটি লোকাল ফোল্ডারে সেভ করা
            video_path = uploaded_file.name
            with open(video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # ব্যাকএন্ডে রিকোয়েস্ট পাঠানোর Payload
            url = "http://127.0.0.1:8000/process-video/"
            payload = {
                "video_filename": video_path,
                "output_video_name": "edited_" + video_path,
                "thumbnail_name": "thumb_" + video_path.split(".")[0] + ".png",
                "category": video_category,
                "mood": video_mood,
                "description": video_description
            }
            
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    st.balloons() 
                    st.success("🎉 অসাধারণ! ভিডিও এডিট এবং থাম্বনেইল সফলভাবে তৈরি হয়ে গেছে!")
                    
                    # আউটপুট ফাইল দেখানোর এবং ডাউনলোড করার অপশন
                    result_data = response.json()
                    edited_video_file = result_data.get('edited_video')
                    thumbnail_file = result_data.get('thumbnail')
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info("🎞️ এডিটেড ভিডিও")
                        if edited_video_file and os.path.exists(edited_video_file):
                            st.video(edited_video_file)
                            with open(edited_video_file, "rb") as f_vid:
                                st.download_button(
                                    label="📥 ভিডিও ডাউনলোড করুন",
                                    data=f_vid,
                                    file_name=edited_video_file,
                                    mime="video/mp4"
                                )
                        else:
                            st.write(edited_video_file)
                            
                    with col2:
                        st.info("🖼️ থাম্বনেইল")
                        if thumbnail_file and os.path.exists(thumbnail_file):
                            st.image(thumbnail_file, use_container_width=True)
                            with open(thumbnail_file, "rb") as f_img:
                                st.download_button(
                                    label="📥 থাম্বনেইল ডাউনলোড করুন",
                                    data=f_img,
                                    file_name=thumbnail_file,
                                    mime="image/png"
                                )
                        else:
                            st.write(thumbnail_file)
                        
                else:
                    st.error(f"রিসপন্স এরর: {response.text}")
            except Exception as e:
                st.error(f"সার্ভারের সাথে সংযোগ স্থাপন করা যায়নি: {e}")