import os
import json
import streamlit as str_web
from google import genai
from google.genai import types
from gtts import gTTS
import io

# 🎨 Layout configuration
str_web.set_page_config(page_title="TabiNavi - Japan Local Guide", layout="centered")
str_web.markdown(
    """
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, div, label { color: #111111 !important; }
    div[data-baseweb="select"] > div {
        background-color: #F0F2F6 !important;
        color: #111111 !important;
    }
    div[data-baseweb="popover"] li {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

api_key = str_web.secrets.get("GEMINI_API_KEY")

if not api_key:
    str_web.error("Secrets ထဲမှာ GEMINI_API_KEY ကို ရှာမတွေ့ပါဘူးဗျာ။")
    str_web.stop()

API_KEY = api_key
client = genai.Client(api_key=api_key)


@str_web.cache_resource
def get_gemini_client(key: str):
    return genai.Client(api_key=key)


try:
    client = get_gemini_client(API_KEY)
except Exception as e:
    str_web.error(f"Client初期化エラー: {e}")

# 🗺️ JSON ဖိုင်ကို လုံခြုံစိတ်ချရသော Exception Handling ဖြင့် ဖတ်ခြင်း
prefecture_city_map = {}
if os.path.exists("japan_data.json"):
    try:
        with open("japan_data.json", "r", encoding="utf-8") as f:
            prefecture_city_map = json.load(f)
    except Exception as e:
        str_web.error(f"JSON Data Error: {e}")
else:
    str_web.warning(
        "⚠️ japan_data.json ဖိုင်ကို ရှာမတွေ့သေးပါဘူးဗျာ။ GitHub ပေါ် ရောက်အောင် တင်ပေးဖို့ လိုအပ်ပါတယ်။"
    )

# --- ☰ SIDEBAR LANGUAGE SETTING ---
language_options = {
    "🇯🇵 日本語 (Japanese)": "Japanese",
    "🇲🇲 Myanmar (မြန်မာဘာသာ)": "Myanmar",
    "🇺🇸 English (🇺🇸)": "English",
    "🇹🇭 ภาษาไทย (Thai)": "Thai",
}
selected_lang_label = str_web.sidebar.selectbox(
    "Language / 行動 / 言語", list(language_options.keys()), index=0
)
language = language_options[selected_lang_label]

# --- 2. MOBILE APP CONTAINER CSS ---
str_web.markdown(
    """
    <style>
    .block-container {
        max-width: 430px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 15px !important;
        padding-right: 15px !important;
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .stApp { background-color: #eef2f5; }
    h1 {
        color: #bc152b !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 24px !important;
        text-align: center;
        font-weight: bold;
    }
    div.stButton > button:first-child {
        background-color: #bc152b;
        color: white;
        border-radius: 10px;
        border: none;
        width: 100%;
        padding: 10px;
        font-weight: bold;
        box-shadow: 0px 2px 6px rgba(188, 21, 43, 0.3);
        transition: 0.2s;
    }
    div.stButton > button:first-child:hover { background-color: #911021; color: #ffffff; }
    .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        border-radius: 10px !important;
        border-left: 6px solid #bc152b !important;
        font-weight: bold !important;
        padding: 12px !important;
        margin-bottom: 5px;
    }
    .stCameraInput > div { border-radius: 15px !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# App Header
str_web.markdown("<h1>🇯🇵 TabiNavi</h1>", unsafe_allow_html=True)
str_web.markdown(
    "<p style='text-align: center; color: #666; font-size: 13px;'>必要な情報だけを、必要な時に。手軽に使える携帯用ガイドツール。</p>",
    unsafe_allow_html=True,
)

# --- 4. USER INTERFACE (SELECTBOXES) ---
prefecture = str_web.selectbox(
    "都道府県 (Prefecture)",
    list(prefecture_city_map.keys()) if prefecture_city_map else [],
    index=None,
    placeholder="--- 選択してください ---",
)

if prefecture:
    available_cities = prefecture_city_map.get(prefecture, [])
    city = str_web.selectbox(
        "都市・地域 (City/Area)",
        available_cities,
        index=None,
        placeholder="--- 選択してください ---",
    )
else:
    city = None

experience_type = str_web.selectbox(
    "アクティビティ (Activity)",
    [
        "地元のスーパーでの買い物と家庭料理の体験",
        "銭湯・温泉のマナーと正しい入浴方法",
        "ローカルバスの正しい乗り方と運賃の支払い方",
        "地域密着型居酒屋での注文方法とマナー",
        "コインランドリーの利用方法とマナー",
        "日本のカプセルホテルやビジネスホテルの賢い利用方法",
        "100円ショップ（ダイソー等）で買える便利な旅行グッズと活用法",
        "新幹線の切符の買い方と正しい乗り方マナー",
        "人気のナイトクラブ・バーの探し方と安全な楽しみ方",
    ],
    index=None,
    placeholder="--- 選択してください ---",
)

interests = str_web.text_input("こだわり条件 (Preference)", "Solo traveler")

# --- 5. FUNCTIONAL SECTIONS ---
str_web.markdown(
    "<hr style='margin: 15px 0; border: none; border-top: 1px solid #ddd;'>",
    unsafe_allow_html=True,
)

if prefecture and city:
    search_query = (
        city.replace("区", "").replace("市", "") + f"+{prefecture.split(' ')[0]}"
    )
    map_url = f"https://maps.google.com/maps?q={search_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"
    str_web.markdown(
        f'<iframe src="{map_url}" width="100%" height="220" style="border:0; border-radius:12px; box-shadow: 0px 2px 8px rgba(0,0,0,0.05);" allowfullscreen="" loading="lazy"></iframe>',
        unsafe_allow_html=True,
    )
    str_web.write("")

common_ai_config = types.GenerateContentConfig(
    temperature=0.7,
    system_instruction=(
        f"You are a hyper-local travel expert. Provide highly detailed, practical step-by-step guidance. "
        f"Strict Rule: Extract and show ONLY the most important main points using short bullet points. Do not write long paragraphs. "
        f"When the output language is Myanmar, use natural, simple, modern colloquial Myanmar prose (စကားပြောဟန်) that is easy to read."
    ),
)

# ----------------- BOX 1. LOCAL ETIGUETTE -----------------
with str_web.expander("🗺️ 1. ローカルマナー＆ガイド"):
    if str_web.button("📝 ガイドを生成", key="btn_guide"):
        if not (prefecture and city and language and experience_type):
            str_web.error("⚠️ 全ての項目を正しく選択してください！")
        else:
            with str_web.spinner("AIガイドを生成中..."):
                prompt = f"Provide a short, bullet-point hyper-local travel guide for '{experience_type}' in {city}, {prefecture} for '{interests}'. Output language: {language}. Keep it brief, focus only on main points. Include 2-3 Google Maps links."
                placeholder = str_web.empty()
                full_text = ""
                try:
                    res_stream = client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=common_ai_config,
                    )
                    for chunk in res_stream:
                        full_text += chunk.text
                        placeholder.markdown(full_text)
                except Exception as e:
                    str_web.error(f"Error: {e}")

# ----------------- BOX 2. WEATHER & OUTFIT -----------------
with str_web.expander("☀️ 2. 現在の天気＆服装ガイド"):
    if str_web.button("🌡️ 天気をチェック", key="btn_weather"):
        if not (prefecture and city and language and experience_type):
            str_web.error("⚠️ 全ての項目を正しく選択してください！")
        else:
            with str_web.spinner("天気情報を分析中..."):
                prompt = f"Estimate seasonal weather trends for this month in {city}, {prefecture} for year 2026. Suggest clothes for '{experience_type}' using short bullet points. Output language: {language}."
                placeholder = str_web.empty()
                full_text = ""
                try:
                    res_stream = client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=common_ai_config,
                    )
                    for chunk in res_stream:
                        full_text += chunk.text
                        placeholder.markdown(full_text)
                except Exception as e:
                    str_web.error(f"Error: {e}")

# ----------------- BOX 3. CURRENCY CONVERTER -----------------
with str_web.expander("💱 3. 通貨両替計算機"):
    currency_target = str_web.selectbox(
        "通貨 (Currency)", ["MMK (Myanmar Kyat)", "USD (US Dollar)"], key="currency_box"
    )
    yen_amount = str_web.number_input("日本円 (JPY)", min_value=0, value=1000, step=500)

    if str_web.button("💰 両替計算する", key="btn_calc"):
        if not (prefecture and city and language and experience_type):
            str_web.error("⚠️ 上記の全ての項目をまず選択してください！")
        else:
            with str_web.spinner("計算中..."):
                prompt = f"Convert {yen_amount} JPY into {currency_target} using realistic 2026 rates. Briefly explain what this can buy for '{experience_type}' in {city} in 2-3 short bullets. Output language: {language}."
                placeholder = str_web.empty()
                full_text = ""
                try:
                    res_stream = client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=common_ai_config,
                    )
                    for chunk in res_stream:
                        full_text += chunk.text
                        placeholder.markdown(full_text)
                except Exception as e:
                    str_web.error(f"Error: {e}")

# ----------------- BOX 4. EMERGENCY SOS -----------------
with str_web.expander("🚨 4. 緊急連絡先＆対応病院"):
    if str_web.button("🏥 緊急情報を表示", key="btn_sos"):
        if not (prefecture and city and language):
            str_web.error("⚠️ 都道府県、都市、言語を選択してください！")
        else:
            with str_web.spinner("検索中..."):
                prompt = f"Provide Japan emergency numbers (110, 119) and 1-2 real hospitals near {city}, {prefecture} supporting foreigners/English using short bullets. Output language: {language}."
                placeholder = str_web.empty()
                full_text = ""
                try:
                    res_stream = client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=common_ai_config,
                    )
                    for chunk in res_stream:
                        full_text += chunk.text
                        placeholder.markdown(full_text)
                except Exception as e:
                    str_web.error(f"Error: {e}")

# --- 6. CAMERA SECTION ---
str_web.markdown(
    "<hr style='margin: 15px 0; border: none; border-top: 1px solid #ddd;'>",
    unsafe_allow_html=True,
)
str_web.markdown(
    "<h3 style='font-size: 18px; color: #bc152b; font-weight: bold;'>📸 メニュー翻訳 ＆ 音声ガイド</h3>",
    unsafe_allow_html=True,
)

if "show_camera" not in str_web.session_state:
    str_web.session_state.show_camera = False

if not str_web.session_state.show_camera:
    if str_web.button("📷 カメラを起動する", key="btn_cam_open"):
        str_web.session_state.show_camera = True
        str_web.rerun()
else:
    if str_web.button("❌ カメラを閉じる", key="btn_cam_close"):
        str_web.session_state.show_camera = False
        str_web.rerun()

if str_web.session_state.show_camera:
    uploaded_file = str_web.camera_input("Take a photo")

    if uploaded_file is not None:
        str_web.image(uploaded_file, caption="撮影された画像", width=280)

        if "menu_text" not in str_web.session_state:
            str_web.session_state.menu_text = ""
        if "japanese_phrase" not in str_web.session_state:
            str_web.session_state.japanese_phrase = "これをお願いします"

        if str_web.button("🥢 メニューを翻訳", key="btn_trans"):
            if not language:
                str_web.error("⚠️ 出力言語(Language)を選択してください！")
            else:
                with str_web.spinner("翻訳中..."):
                    image_bytes = uploaded_file.getvalue()
                    image_part = types.Part.from_bytes(
                        data=image_bytes, mime_type="image/jpeg"
                    )

                    menu_prompt = f"""
                    Translate this Japanese menu into {language}. Briefly explain dishes/ingredients using short bullet points.
                    Extract 1 key phrase to order food (Write ONLY Japanese Kanji/Kana after 'PHRASE:', e.g., PHRASE:これをお願いします)
                    """
                    menu_placeholder = str_web.empty()
                    menu_text = ""
                    try:
                        res_stream = client.models.generate_content_stream(
                            model="gemini-2.5-flash",
                            contents=[image_part, menu_prompt],
                            config=common_ai_config,
                        )
                        for chunk in res_stream:
                            menu_text += chunk.text
                            menu_placeholder.markdown(menu_text)
                        str_web.session_state.menu_text = menu_text
                        if "PHRASE:" in menu_text:
                            str_web.session_state.japanese_phrase = menu_text.split(
                                "PHRASE:"
                            )[-1].strip()
                    except Exception as menu_err:
                        str_web.error(f"Error: {menu_err}")

        if str_web.session_state.menu_text:
            str_web.write("🔊 **日本語の音声を再生:**")
            if str_web.button("🗣️ 再生", key="btn_voice"):
                try:
                    tts = gTTS(text=str_web.session_state.japanese_phrase, lang="ja")
                    sound_file = io.BytesIO()
                    tts.write_to_fp(sound_file)
                    str_web.audio(sound_file.getvalue(), format="audio/mp3")
                except Exception as voice_err:
                    str_web.error(f"Error: {voice_err}")
