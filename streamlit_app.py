import streamlit as st
import openai

# 🔑 OpenAI API 키 입력
openai.api_key = "YOUR_OPENAI_API_KEY"  # ← 여기에 본인 키 입력

st.set_page_config(page_title="LifeCast – 연애 4컷 시나리오 생성기", layout="wide")
st.title("🎞️ LifeCast – 자유서술 + 이미지/영상 기반 4컷 만화 생성기")

st.markdown("""
당신의 연애 이야기를 텍스트, 이미지, 영상, 음성으로 남겨주세요.  
AI가 이를 바탕으로 **4컷 만화 시놉시스**를 생성해드립니다.
""")

# 사용자 입력
with st.expander("📝 연애 이야기 자유서술", expanded=True):
    story_text = st.text_area("당신의 연애 이야기를 자유롭게 입력해주세요 (200자 이상)", height=300)

# 멀티미디어 입력
with st.expander("🖼️ 미디어 업로드"):
    uploaded_images = st.file_uploader("📸 이미지 업로드 (선택, 여러 장 가능)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    uploaded_videos = st.file_uploader("🎥 영상 업로드 (선택)", type=["mp4", "mov", "avi"], accept_multiple_files=True)
    uploaded_audio = st.file_uploader("🎙️ 음성 업로드 (선택)", type=["mp3", "wav"], accept_multiple_files=True)

# 버튼 클릭 시 시놉시스 생성
if st.button("✅ 4컷 시나리오 생성"):
    if not story_text or len(story_text.strip()) < 100:
        st.warning("조금 더 자세히 입력해 주세요. (최소 100자 이상 권장)")
    else:
        with st.spinner("AI가 4컷으로 정리 중입니다..."):

            # GPT 프롬프트 구성
            prompt = f"""
다음은 사용자가 작성한 연애 이야기입니다.  
이 이야기를 바탕으로 다음 형식으로 4컷 만화 시나리오를 작성해 주세요:

형식:
1컷: [인연의 시작] - 장면 설명 (200자 내외)
2컷: [가까워진 계기] - 장면 설명
3컷: [갈등 혹은 전환점] - 장면 설명
4컷: [결말 또는 회고] - 장면 설명 + 감정

연애 이야기:
\"\"\"{story_text}\"\"\"

4컷 시놉시스:
"""

            # GPT 호출
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )

            result = response['choices'][0]['message']['content']
            st.success("✅ 시놉시스 생성 완료!")
            st.markdown(result)

            st.divider()

            # 미디어 출력
            st.subheader("🖼️ 함께 업로드한 미디어")

            if uploaded_images:
                st.markdown("**📸 이미지**")
                for img in uploaded_images:
                    st.image(img, use_column_width=True)

            if uploaded_videos:
                st.markdown("**🎥 영상**")
                for vid in uploaded_videos:
                    st.video(vid)

            if uploaded_audio:
                st.markdown("**🎙️ 음성**")
                for aud in uploaded_audio:
                    st.audio(aud)
