import os
import json
import streamlit as str_web
from google import genai
from google.genai import types

# 🎨 Streamlit Configuration & Title
str_web.set_page_config(page_title="TabiNavi", layout="centered")

# --- 🌐 MULTI-LANGUAGE DICTIONARY FOR UI ---
ui_translations = {
    "English": {
        "title": "🇯🇵 TabiNavi",
        "sub": "Essential local information, right when you need it.",
        "pref_label": "📍 Select Prefecture",
        "pref_holder": "Choose a prefecture...",
        "city_label": "🏙️ Select City / Area",
        "city_holder": "Choose a city...",
        "city_warn": "Please select a prefecture first.",
        "sec_trip": "🎯 Trip Activities",
        "act_label": "Select Activity Type",
        "act_holder": "Choose an activity...",
        "guide_box": "📝 1. Local Etiquette & Guide",
        "guide_btn": "Generate Guide",
        "weather_box": "🌤️ 2. Weather & Clothing Guide",
        "weather_btn": "Check Weather",
        "calc_box": "💱 3. Currency Converter",
        "calc_btn": "Calculate",
        "sos_box": "🚨 4. Emergency SOS & Hospitals",
        "sos_btn": "Show Emergency Contacts",
        "error_select": "⚠️ Please select Prefecture, City, and Activity first!",
        "sidebar_title": "⚙️ Settings",
    },
    "Myanmar": {
        "title": "🇯🇵 TabiNavi",
        "sub": "လိုအပ်မည့် ဒေသတွင်းအချက်အလက်များကို အချိန်မရွေး ကြည့်ရှုနိုင်မည့် လမ်းညွှန်။",
        "pref_label": "📍 ပြည်နယ်/ခရိုင် ကို ရွေးချယ်ပါ",
        "pref_holder": "ခရိုင်တစ်ခု ရွေးချယ်ပေးပါ...",
        "city_label": "🏙️ မြို့/ဒေသ ကို ရွေးချယ်ပါ",
        "city_holder": "မြို့ကို ရွေးချယ်ပေးပါ...",
        "city_warn": "အပေါ်တွင် ခရိုင်တစ်ခု အရင်ရွေးပေးပါ။",
        "sec_trip": "🎯 ပြုလုပ်မည့် အတွေ့အကြုံများ",
        "act_label": "လုပ်ဆောင်မည့် အတွေ့အကြုံ အမျိုးအစား",
        "act_holder": "အတွေ့အကြုံ ရွေးချယ်ရန်...",
        "guide_box": "📝 ၁။ ဒေသတွင်း လမ်းညွှန်နှင့် စည်းကမ်းများ",
        "guide_btn": "လမ်းညွှန်ချက် ထုတ်လုပ်မည်",
        "weather_box": "🌤️ ၂။ လက်ရှိရာသီဥတုနှင့် ဝတ်စားဆင်ယင်မှု လမ်းညွှန်",
        "weather_btn": "ရာသီဥတုနှင့် ဝတ်ဆင်ရမည့်ပုံစံ စစ်မည်",
        "calc_box": "💱 ၃။ ငွေလဲနှုန်း တွက်ချက်စနစ်",
        "calc_btn": "ငွေလဲနှုန်း တွက်မည်",
        "sos_box": "🚨 ၄။ အရေးပေါ် ဖုန်းနံပါတ်များနှင့် ဆေးရုံများ",
        "sos_btn": "အရေးပေါ် အချက်အလက်ပြပါ",
        "error_select": "⚠️ ကျေးဇူးပြု၍ ခရိုင်၊ မြို့နှင့် လုပ်ဆောင်ချက်များကို အရင်ရွေးချယ်ပေးပါဦးဗျာ။",
        "sidebar_title": "⚙️ ဆက်တင်များ",
    },
    "Japanese": {
        "title": "🇯🇵 TabiNavi",
        "sub": "必要な情報だけを、必要な時に。手軽に使える携帯用ガイドツール。",
        "pref_label": "📍 都道府県を選択",
        "pref_holder": "都道府県を選んでください...",
        "city_label": "🏙️ 都市・地域を選択",
        "city_holder": "都市を選んでください...",
        "city_warn": "最初に都道府県を選択してください。",
        "sec_trip": "🎯 旅行のアクティビティ",
        "act_label": "アクティビティのタイプ",
        "act_holder": "アクティビティを選択...",
        "guide_box": "📝 1. ローカルマナー ＆ ガイド",
        "guide_btn": "ガイドを生成",
        "weather_box": "🌤️ 2. 現在の天気 ＆ 服装ガイド",
        "weather_btn": "天気と服装をチェック",
        "calc_box": "💱 3. 通貨両替計算機",
        "calc_btn": "計算する",
        "sos_box": "🚨 4. 緊急連絡先 ＆ 対応病院",
        "sos_btn": "緊急情報を表示",
        "error_select": "⚠️ 全ての項目を正しく選択してください！",
        "sidebar_title": "⚙️ 設定",
    },
}

# --- ⚙️ SIDEBAR SETTINGS (FotMob Style) ---
with str_web.sidebar:
    str_web.markdown("### ⚙️ Settings")

    # 1. Language Dropdown inside Sidebar
    language_options = {
        "🇺🇸 English": "English",
        "🇲🇲 Myanmar (မြန်မာ)": "Myanmar",
        "🇯🇵 日本語": "Japanese",
    }
    selected_lang_label = str_web.selectbox(
        "Select interface language", list(language_options.keys()), index=0
    )
    current_lang = language_options[selected_lang_label]
    tx = ui_translations[current_lang]

    str_web.markdown("<br>", unsafe_allow_html=True)

    # 2. Theme Selector inside Sidebar
    theme_choice = str_web.radio(
        "Theme Mode", ["⚙️ System Default (Dark)", "☀️ Classic White"], index=0
    )

# --- 🎨 ULTRA PREMIUM CLEAN CSS INJECTION ---
if "System Default (Dark)" in theme_choice:
    # Beautiful FotMob Premium Dark UI
    str_web.markdown(
        """
        <style>
        .stApp { background-color: #0b0e11 !important; color: #ffffff !important; }
        .block-container {
            max-width: 430px !important;
            padding: 25px 20px !important;
            background-color: #111417 !important;
            border-radius: 24px;
            box-shadow: 0px 12px 40px rgba(0, 0, 0, 0.6);
            margin-top: 20px;
        }
        h1, h2, h3, p, label { color: #ffffff !important; font-family: -apple-system, sans-serif; }
        div[data-baseweb="select"] > div, .stTextInput div div input {
            background-color: #1c2024 !important;
            border: 1px solid #2c3136 !important;
            border-radius: 16px !important;
            color: #ffffff !important;
        }
        div[data-baseweb="popover"] ul { background-color: #1c2024 !important; }
        div[data-baseweb="popover"] li { color: #ffffff !important; background-color: #1c2024 !important; }
        div[data-baseweb="popover"] li:hover { background-color: #2c3136 !important; }
        .streamlit-expanderHeader { 
            background-color: #1c2024 !important; 
            color: #ffffff !important; 
            border-radius: 16px !important; 
            border: 1px solid #2c3136 !important;
            margin-bottom: 10px;
            padding: 12px !important;
        }
        .streamlit-expanderContent { background-color: #1c2024 !important; color: #ffffff !important; border-radius: 16px; }
        div.stButton > button:first-child { 
            background-color: #22c55e !important; 
            color: white !important; 
            border-radius: 14px !important; 
            border: none !important;
            width: 100%; 
            font-weight: bold;
        }
        hr { border-color: #2c3136 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    # Clean Classic White UI
    str_web.markdown(
        """
        <style>
        .stApp { background-color: #f4f6f9 !important; color: #1c1c1e !important; }
        .block-container {
            max-width: 430px !important;
            padding: 25px 20px !important;
            background-color: #ffffff !important;
            border-radius: 24px;
            box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.05);
            margin-top: 20px;
        }
        h1, p, label { color: #1c1c1e !important; font-family: -apple-system, sans-serif; }
        div[data-baseweb="select"] > div { background-color: #f2f4f7 !important; border-radius: 16px !important; }
        .streamlit-expanderHeader { background-color: #f2f4f7 !important; color: #1c1c1e !important; border-radius: 16px !important; margin-bottom: 10px; }
        .streamlit-expanderContent { background-color: #f2f4f7 !important; color: #1c1c1e !important; }
        div.stButton > button:first-child { background-color: #007aff !important; color: white !important; border-radius: 14px !important; width: 100%; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- API CLIENT & DATA SETUP ---
api_key = str_web.secrets.get("GEMINI_API_KEY")
if not api_key:
    str_web.error("Secrets ထဲမှာ GEMINI_API_KEY ကို ရှာမတွေ့ပါဘူးဗျာ။")
    str_web.stop()

client = genai.Client(api_key=api_key)

prefecture_city_map = {}
if os.path.exists("japan_data.json"):
    try:
        with open("japan_data.json", "r", encoding="utf-8") as f:
            prefecture_city_map = json.load(f)
    except Exception as e:
        str_web.error(f"JSON Data Error: {e}")

# --- MAIN APP DISPLAY ---
str_web.markdown(
    f"<h1 style='text-align: center; font-size: 26px; font-weight: 800; letter-spacing: -0.5px;'>{tx['title']}</h1>",
    unsafe_allow_html=True,
)
str_web.markdown(
    f"<p style='text-align: center; font-size: 13px; color: #8e8e93; margin-bottom: 30px; line-height: 1.4;'>{tx['sub']}</p>",
    unsafe_allow_html=True,
)

# 1. Prefecture Dropdown
prefecture = str_web.selectbox(
    tx["pref_label"],
    list(prefecture_city_map.keys()) if prefecture_city_map else [],
    index=None,
    placeholder=tx["pref_holder"],
)

# 2. City Dropdown
if prefecture:
    available_cities = prefecture_city_map.get(prefecture, [])
    city = str_web.selectbox(
        tx["city_label"], available_cities, index=None, placeholder=tx["city_holder"]
    )
else:
    city = None
    str_web.markdown(
        f"<p style='font-size: 12px; color: #8e8e93; margin-left:5px;'>{tx['city_warn']}</p>",
        unsafe_allow_html=True,
    )

# --- SECTION 2: TRIP ACTIVITIES ---
str_web.markdown("<hr>", unsafe_allow_html=True)
str_web.markdown(
    f"<div style='font-size:16px; font-weight:700; margin-bottom:12px; letter-spacing: -0.2px;'>{tx['sec_trip']}</div>",
    unsafe_allow_html=True,
)

activity_mapping = {
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
    "Japanese": [
        "地元のスーパーでの買い物と家庭料理の体験",
        "銭湯・温泉のマナーと正しい入浴方法",
        "ローカルバスの正しい乗り方と運賃の支払い方",
        "地域密着型居酒屋での注文方法とマナー",
        "コインランドリーの利用方法とマナー",
        "日本のカプセルホテルやビジネスホテルの賢い利用方法",
    ],
}

experience_type = str_web.selectbox(
    tx["act_label"],
    activity_mapping[current_lang],
    index=None,
    placeholder=tx["act_holder"],
)

# --- MAPS INTEGRATION ---
if prefecture and city:
    str_web.markdown("<br>", unsafe_allow_html=True)
    search_query = (
        city.replace("区", "").replace("市", "") + f"+{prefecture.split(' ')[0]}"
    )
    map_url = f"https://maps.google.com/maps?q={search_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"
    str_web.markdown(
        f'<iframe src="{map_url}" width="100%" height="160" style="border:0; border-radius:16px;" allowfullscreen="" loading="lazy"></iframe>',
        unsafe_allow_html=True,
    )

# --- SECTION 3: FEATURES & TOOLS (WITH WEATHER) ---
str_web.markdown("<br>", unsafe_allow_html=True)

common_ai_config = types.GenerateContentConfig(
    temperature=0.7,
    system_instruction=f"You are a local travel expert. Provide output strictly in short bullet points. Output language: {current_lang}.",
)

# Box 1: Local Guide
with str_web.expander(tx["guide_box"]):
    if str_web.button(tx["guide_btn"], key="btn_guide"):
        if not (prefecture and city and experience_type):
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("Loading..."):
                prompt = f"Provide a brief bullet-point local guide for '{experience_type}' in {city}, {prefecture}."
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash", contents=prompt, config=common_ai_config
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

# Box 2: Weather & Clothing Guide (ပြန်လည်ထည့်သွင်းထားသည်)
with str_web.expander(tx["weather_box"]):
    if str_web.button(tx["weather_btn"], key="btn_weather"):
        if not (prefecture and city):
            str_web.error("⚠️ Please select Prefecture and City first!")
        else:
            with str_web.spinner("Loading..."):
                prompt = f"Provide typical 2026 current month weather forecast statistics for {city}, {prefecture} and recommend what to wear in short bullets."
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash", contents=prompt, config=common_ai_config
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

# Box 3: Currency Converter
with str_web.expander(tx["calc_box"]):
    currency_target = str_web.selectbox(
        "Target Currency", ["MMK (Myanmar Kyat)", "USD (US Dollar)"]
    )
    yen_amount = str_web.number_input(
        "Amount in JPY", min_value=0, value=1000, step=500
    )
    if str_web.button(tx["calc_btn"], key="btn_calc"):
        with str_web.spinner("Calculating..."):
            prompt = f"Convert {yen_amount} JPY into {currency_target} using realistic 2026 rates. List what it can buy in 2 bullets."
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash", contents=prompt, config=common_ai_config
            ):
                full_text += chunk.text
                placeholder.markdown(full_text)

# Box 4: SOS Emergency
with str_web.expander(tx["sos_box"]):
    if str_web.button(tx["sos_btn"], key="btn_sos"):
        with str_web.spinner("Loading..."):
            prompt = f"Provide Japan emergency numbers and 1 hospital near {city if city else 'Tokyo'} supporting foreigners."
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash", contents=prompt, config=common_ai_config
            ):
                full_text += chunk.text
                placeholder.markdown(full_text)
