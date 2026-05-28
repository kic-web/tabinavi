import os
import json
import streamlit as str_web
from google import genai
from google.genai import types
from gtts import gTTS
import io

# 🎨 Premium Mobile View Setup & Custom Dark-Mode Inspired UI
str_web.set_page_config(page_title="TabiNavi - Settings", layout="centered")

# --- ⚙️ FOTMOB STYLE CSS INJECTION ---
str_web.markdown(
    """
    <style>
    .stApp { background-color: #0b0e11 !important; }
    .block-container {
        max-width: 430px !important;
        padding: 25px 20px !important;
        background-color: #000000 !important;
        border-radius: 25px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
        margin-top: 15px;
        margin-bottom: 15px;
    }
    h1 {
        color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 24px !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 5px !important;
    }
    .section-title {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-top: 25px !important;
        margin-bottom: 12px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #1c1c1e !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 6px 10px !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #ffffff !important;
        font-size: 15px !important;
    }
    div[data-baseweb="popover"] ul { background-color: #1c1c1e !important; }
    div[data-baseweb="popover"] li { background-color: #1c1c1e !important; color: #ffffff !important; }
    div[data-baseweb="popover"] li:hover { background-color: #2c2c2e !important; }
    label {
        color: #8e8e93 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 5px;
        margin-bottom: 6px !important;
    }
    div.stButton > button:first-child {
        background-color: #bc152b !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        width: 100%;
        padding: 12px !important;
        font-weight: bold !important;
    }
    .streamlit-expanderHeader {
        background-color: #1c1c1e !important;
        border: none !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        margin-bottom: 10px;
    }
    .streamlit-expanderContent { background-color: #1c1c1e !important; color: #ffffff !important; }
    hr { border-color: #2c2c2e !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- API CLIENT & JSON SETUP ---
api_key = str_web.secrets.get("GEMINI_API_KEY")
if not api_key:
    str_web.error("Secrets ထဲမှာ GEMINI_API_KEY ကို ရှာမတွေ့ပါဘူးဗျာ।")
    str_web.stop()

client = genai.Client(api_key=api_key)

prefecture_city_map = {}
if os.path.exists("japan_data.json"):
    try:
        with open("japan_data.json", "r", encoding="utf-8") as f:
            prefecture_city_map = json.load(f)
    except Exception as e:
        str_web.error(f"JSON Data Error: {e}")

# 🌐 MULTI-LANGUAGE DICTIONARY FOR UI
ui_translations = {
    "Japanese": {
        "title": "⚙️ 設定 (Settings)",
        "sub": "ローカル旅行の設定を行います",
        "sec_general": "一般設定",
        "pref_label": "📍 都道府県を選択",
        "pref_holder": "都道府県を選んでください...",
        "city_label": "🏙️ 都市・地域を選択",
        "city_holder": "都市を選んでください...",
        "city_warn": "都市を有効にするには、まず都道府県を選択してください。",
        "sec_trip": "旅行の好み",
        "act_label": "🎯 アクティビティのタイプ",
        "act_holder": "アクティビティを選択...",
        "sec_other": "その他のガイド＆ツール",
        "guide_box": "📝 ローカルガイド ＆ マナーサポート",
        "guide_btn": "ガイドを生成",
        "calc_box": "💱 通貨両替計算機",
        "calc_btn": "両替計算する",
        "sos_box": "🚨 緊急連絡先 ＆ 対応病院",
        "sos_btn": "緊急情報を表示",
        "sec_cam": "スマート翻訳機",
        "cam_btn_open": "📷 メニューカメラ起動",
        "cam_btn_close": "❌ カメラを閉じる",
        "cam_trans": "🥢 メニューを翻訳",
        "error_select": "⚠️ 全ての項目を正しく選択してください！",
    },
    "English": {
        "title": "⚙️ Settings",
        "sub": "Configure your local travel preferences",
        "sec_general": "General Settings",
        "pref_label": "📍 Select Prefecture",
        "pref_holder": "Choose a prefecture...",
        "city_label": "🏙️ Select City / Area",
        "city_holder": "Choose a city...",
        "city_warn": "Please select a prefecture first to unlock cities.",
        "sec_trip": "Trip Preferences",
        "act_label": "🎯 Activity Type",
        "act_holder": "Select activity...",
        "sec_other": "Other Guides & Tools",
        "guide_box": "📝 Tips and support (Local Guide)",
        "guide_btn": "Generate Guide",
        "calc_box": "💱 Currency Converter",
        "calc_btn": "Calculate Conversion",
        "sos_box": "🚨 Emergency SOS Numbers",
        "sos_btn": "Show Emergency Contacts",
        "sec_cam": "Smart Translator",
        "cam_btn_open": "📷 Open Menu Camera",
        "cam_btn_close": "❌ Close Camera",
        "cam_trans": "🥢 Translate Menu",
        "error_select": "⚠️ Please select Prefecture, City, and Activity first!",
    },
    "Myanmar": {
        "title": "⚙️ ဆက်တင်များ (Settings)",
        "sub": "သင်သွားမည့် ဒေသတွင်းခရီးစဉ် စိတ်ကြိုက်ပြင်ဆင်ရန်",
        "sec_general": "အထွေထွေ ဆက်တင်များ",
        "pref_label": "📍 ပြည်နယ်/ခရိုင် ကို ရွေးချယ်ပါ",
        "pref_holder": "ခရိုင်တစ်ခု ရွေးချယ်ပေးပါ...",
        "city_label": "🏙️ မြို့/ဒေသ ကို ရွေးချယ်ပါ",
        "city_holder": "မြို့ကို ရွေးချယ်ပေးပါ...",
        "city_warn": "မြို့များကို ရွေးချယ်နိုင်ရန် အရင်ဆုံး ခရိုင်တစ်ခုကို အပေါ်တွင် ရွေးပေးပါရန်။",
        "sec_trip": "ခရီးစဉ် စိတ်ကြိုက်ရွေးချယ်မှု",
        "act_label": "🎯 လုပ်ဆောင်မည့် အတွေ့အကြုံ အမျိုးအစား",
        "act_holder": "အတွေ့အကြုံ ရွေးချယ်ရန်...",
        "sec_other": "အခြား လမ်းညွှန်များနှင့် ကိရိယာများ",
        "guide_box": "📝 ဒေသတွင်း လမ်းညွှန်နှင့် ယဉ်ကျေးမှု စည်းကမ်းများ",
        "guide_btn": "လမ်းညွှန်ချက် ထုတ်လုပ်မည်",
        "calc_box": "💱 ငွေလဲနှုန်း တွက်ချက်စနစ်",
        "calc_btn": "ငွေလဲနှုန်း တွက်မည်",
        "sos_box": "🚨 အရေးပေါ် ဖုန်းနံပါတ်များနှင့် ဆေးရုံများ",
        "sos_btn": "အရေးပေါ် အချက်အလက်ပြပါ",
        "sec_cam": "စမတ်ကင်မရာ ဘာသာပြန်စနစ်",
        "cam_btn_open": "📷 မီနူးဖတ်ရန် ကင်မရာဖွင့်မည်",
        "cam_btn_close": "❌ ကင်မရာ ပြန်ပိတ်မည်",
        "cam_trans": "🥢 မီနူးကို ဘာသာပြန်မည်",
        "error_select": "⚠️ ကျေးဇူးပြု၍ ခရိုင်၊ မြို့နှင့် လုပ်ဆောင်ချက်များကို အရင်ရွေးချယ်ပေးပါဦးဗျာ။",
    },
}

# --- 🌐 LANGUAGE DROPDOWN ---
language_options = {
    "🇺🇸 English (🇺🇸)": "English",
    "🇲🇲 Myanmar (မြန်မာဘာသာ)": "Myanmar",
    "🇯🇵 日本語 (Japanese)": "Japanese",
}

selected_lang_label = str_web.selectbox(
    "Select Interface Language / 言語選択", list(language_options.keys()), index=0
)
current_lang = language_options[selected_lang_label]
tx = ui_translations[current_lang]

# --- APP HEADER ---
str_web.markdown(f"<h1>{tx['title']}</h1>", unsafe_allow_html=True)
str_web.markdown(
    f"<p style='text-align: center; color: #8e8e93; font-size: 13px; margin-bottom: 20px;'>{tx['sub']}</p>",
    unsafe_allow_html=True,
)

# ----------------- SECTION 1: GENERAL SETTINGS -----------------
str_web.markdown(
    f"<div class='section-title'>{tx['sec_general']}</div>", unsafe_allow_html=True
)

# 1. Prefecture Row
prefecture = str_web.selectbox(
    tx["pref_label"],
    list(prefecture_city_map.keys()) if prefecture_city_map else [],
    index=None,
    placeholder=tx["pref_holder"],
)

# 2. City Row
if prefecture:
    available_cities = prefecture_city_map.get(prefecture, [])
    city = str_web.selectbox(
        tx["city_label"], available_cities, index=None, placeholder=tx["city_holder"]
    )
else:
    city = None
    str_web.markdown(
        f"<p style='color: #48484a; font-size: 13px; margin-left: 5px;'>{tx['city_warn']}</p>",
        unsafe_allow_html=True,
    )

# ----------------- SECTION 2: TRIP PREFERENCES -----------------
str_web.markdown(
    f"<div class='section-title'>{tx['sec_trip']}</div>", unsafe_allow_html=True
)

activity_mapping = {
    "Japanese": [
        "地元のスーパーでの買い物と家庭料理の体験",
        "銭湯・温泉のマナーと正しい入浴方法",
        "ローカルバスの正しい乗り方と運賃の支払い方",
        "地域密着型居酒屋での注文方法とマナー",
        "コインランドリーの利用方法とマナー",
        "日本のカプセルホテルやビジネスホテルの賢い利用方法",
    ],
    "English": [
        "Shopping at local supermarkets & home cooking experience",
        "Sento/Onsen etiquette & correct bathing method",
        "How to ride local buses and pay the fare correctly",
        "Ordering food & manners at local Izakaya",
        "Coin laundry usage guidelines and manners",
        "Smart utilization of Japanese Capsule Hotels or Business Hotels",
    ],
    "Myanmar": [
        "ဒေသတွင်းစူပါမားကတ်တွင် ဈေးဝယ်ခြင်းနှင့် အိမ်ချက်ချက်ပြုတ်မှု အတွေ့အကြုံ",
        "အများသုံးရေချိုးခန်း (Sento/Onsen) စည်းကမ်းနှင့် စနစ်တကျ ရေချိုးနည်း",
        "ဒေသန္တရဘတ်စ်ကားများ စနစ်တကျစီးနင်းခြင်းနှင့် ကားခပေးချေနည်း",
        "ဒေသတွင်း အီဇာကာယ (Izakaya) ဆိုင်များတွင် မှာယူနည်းနှင့် စည်းကမ်းများ",
        "အကြွေစေ့သုံး အဝတ်လျှော်စက် (Coin Laundry) အသုံးပြုနည်း လမ်းညွှန်",
        "ဂျပန်နိုင်ငံရှိ Capsule ဟိုတယ်များနှင့် စီးပွားရေးဟိုတယ်များကို စမတ်ကျကျ အသုံးပြုနည်း",
    ],
}

# 3. Activity Row (Preference အကွက်အား လုံးဝဖယ်ရှားပြီးဖြစ်သည်)
experience_type = str_web.selectbox(
    tx["act_label"],
    activity_mapping[current_lang],
    index=None,
    placeholder=tx["act_holder"],
)

# --- MAPS TOOL ---
if prefecture and city:
    str_web.markdown("<br>", unsafe_allow_html=True)
    search_query = (
        city.replace("区", "").replace("市", "") + f"+{prefecture.split(' ')[0]}"
    )
    map_url = f"https://maps.google.com/maps?q={search_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"
    str_web.markdown(
        f'<iframe src="{map_url}" width="100%" height="180" style="border:0; border-radius:14px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" allowfullscreen="" loading="lazy"></iframe>',
        unsafe_allow_html=True,
    )

# ----------------- SECTION 3: FEATURES & TOOLS -----------------
str_web.markdown(
    f"<div class='section-title'>{tx['sec_other']}</div>", unsafe_allow_html=True
)

common_ai_config = types.GenerateContentConfig(
    temperature=0.7,
    system_instruction=(
        f"You are a hyper-local travel expert. Provide highly detailed, practical step-by-step guidance. "
        f"Strict Rule: Extract and show ONLY the most important main points using short bullet points. Do not write long paragraphs. "
        f"Output everything strictly in the language requested: {current_lang}."
    ),
)

# Box 1: Local Guide
with str_web.expander(tx["guide_box"]):
    if str_web.button(tx["guide_btn"], key="btn_guide"):
        if not (prefecture and city and experience_type):
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("Loading..."):
                prompt = f"Provide a short, bullet-point hyper-local travel guide for '{experience_type}' in {city}, {prefecture}. Respond in {current_lang} language."
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash", contents=prompt, config=common_ai_config
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

# Box 2: Currency Converter
with str_web.expander(tx["calc_box"]):
    currency_target = str_web.selectbox(
        "Target Currency", ["MMK (Myanmar Kyat)", "USD (US Dollar)"]
    )
    yen_amount = str_web.number_input(
        "Amount in JPY", min_value=0, value=1000, step=500
    )
    if str_web.button(tx["calc_btn"], key="btn_calc"):
        with str_web.spinner("Calculating..."):
            prompt = f"Convert {yen_amount} JPY into {currency_target} using realistic 2026 rates. Explain what it can buy in {current_lang}."
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash", contents=prompt, config=common_ai_config
            ):
                full_text += chunk.text
                placeholder.markdown(full_text)

# Box 3: SOS
with str_web.expander(tx["sos_box"]):
    if str_web.button(tx["sos_btn"], key="btn_sos"):
        with str_web.spinner("Loading..."):
            prompt = f"Provide Japan emergency numbers and 1 hospital near {city if city else 'Tokyo'} supporting foreigners. Output language: {current_lang}."
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash", contents=prompt, config=common_ai_config
            ):
                full_text += chunk.text
                placeholder.markdown(full_text)

# ----------------- SECTION 4: SMART CAMERA TRANSLATOR -----------------
str_web.markdown(
    f"<div class='section-title'>{tx['sec_cam']}</div>", unsafe_allow_html=True
)

if "show_camera" not in str_web.session_state:
    str_web.session_state.show_camera = False

if not str_web.session_state.show_camera:
    if str_web.button(tx["cam_btn_open"], key="btn_cam_open"):
        str_web.session_state.show_camera = True
        str_web.rerun()
else:
    if str_web.button(tx["cam_btn_close"], key="btn_cam_close"):
        str_web.session_state.show_camera = False
        str_web.rerun()

if str_web.session_state.show_camera:
    uploaded_file = str_web.camera_input("Scan Japanese Menu")
    if uploaded_file is not None:
        str_web.image(uploaded_file, caption="Scanned Image", width=280)

        if str_web.button(tx["cam_trans"], key="btn_trans"):
            with str_web.spinner("Translating..."):
                image_part = types.Part.from_bytes(
                    data=uploaded_file.getvalue(), mime_type="image/jpeg"
                )
                menu_prompt = f"Translate this Japanese menu into {current_lang}. Short bullet points only."
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=[image_part, menu_prompt],
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)
