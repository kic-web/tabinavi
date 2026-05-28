import os
import json
import streamlit as str_web
from google import genai
from google.genai import types

# 🎨 Streamlit Configuration (Native clean design)
str_web.set_page_config(page_title="TabiNavi", layout="centered")

# --- 🌐 MULTI-LANGUAGE DICTIONARY ---
ui_translations = {
    "English": {
        "title": "🇯🇵 TabiNavi",
        "sub": "Essential local information, right when you need it.",
        "pref_label": "📍 Select Prefecture",
        "pref_holder": "Choose a prefecture...",
        "city_label": "🏙️ Select City / Area",
        "city_holder": "Choose a city...",
        "city_warn": "Please select a prefecture first.",
        "sec_quick": "🚀 Quick Travel Services",
        "train_btn": "🚄 Train & Routes",
        "food_btn": "🍣 Food & Dining",
        "hotel_btn": "🏨 Hotel Booking",
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
        "error_select": "⚠️ Please select Prefecture and City first!",
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
        "sec_quick": "🚀 အမြန်အသုံးပြုနိုင်မည့် ဝန်ဆောင်မှုများ",
        "train_btn": "🚄 ရထားလမ်းကြောင်းရှာရန်",
        "food_btn": "🍣 အစားအသောက်နှင့် ဆိုင်များ",
        "hotel_btn": "🏨 ဟိုတယ်နှင့် တည်းခိုခန်းများ",
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
        "error_select": "⚠️ ကျေးဇူးပြု၍ ခရိုင်နှင့် မြို့ကို အရင်ရွေးချယ်ပေးပါဦးဗျာ။",
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
        "sec_quick": "🚀 クイック旅行サービス",
        "train_btn": "🚄 電車・乗換案内",
        "food_btn": "🍣 グルメ・レストラン",
        "hotel_btn": "🏨 ホテル・宿泊予約",
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
        "error_select": "⚠️ 都道府県と都市を正しく選択してください！",
        "sidebar_title": "⚙️ 設定",
    },
}

# --- ⚙️ SIDEBAR SETTINGS ---
with str_web.sidebar:
    str_web.markdown(f"## {ui_translations['English']['sidebar_title']}")
    language_options = {
        "🇺🇸 English": "English",
        "🇲🇲 Myanmar (မြန်မာ)": "Myanmar",
        "🇯🇵 日本語": "Japanese",
    }
    selected_lang_label = str_web.selectbox(
        "🌐 Language", list(language_options.keys()), index=0
    )
    current_lang = language_options[selected_lang_label]
    tx = ui_translations[current_lang]
    str_web.markdown("---")

# --- API CLIENT & DATA SETUP ---
api_key = str_web.secrets.get("GEMINI_API_KEY")
if not api_key:
    str_web.error("Secrets ထဲမှာ GEMINI_API_KEY ကို ရှာမတွေ့ပါဘူးဗျာ။")
    str_web.stop()

client = genai.Client(api_key=api_key)

prefecture_city_map = {}
if os.path.exists("japan_data.json"):
    with open("japan_data.json", "r", encoding="utf-8") as f:
        prefecture_city_map = json.load(f)

# --- MAIN APP DISPLAY ---
str_web.title(tx["title"])
str_web.caption(tx["sub"])

# 1. Location Selection (ခရိုင်နဲ့ မြို့ရွေးချယ်မှု)
prefecture = str_web.selectbox(
    tx["pref_label"],
    list(prefecture_city_map.keys()) if prefecture_city_map else [],
    index=None,
    placeholder=tx["pref_holder"],
)

if prefecture:
    city = str_web.selectbox(
        tx["city_label"],
        prefecture_city_map.get(prefecture, []),
        index=None,
        placeholder=tx["city_holder"],
    )
else:
    city = None
    str_web.markdown(
        f"<p style='font-size: 13px; color: gray;'>{tx['city_warn']}</p>",
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------
# 🚀 NEW FEATURES SECTION (ရထား၊ အစားအသောက်၊ ဟိုတယ်ကို အပေါ်ဆုံးတွင် ထားခြင်း)
# ----------------------------------------------------------------------
str_web.markdown("---")
str_web.subheader(tx["sec_quick"])

# ဘေးတိုက် ကော်လံ ၃ ခု ခွဲလိုက်တာပါဗျာ (App UI ပုံစံထွက်အောင်)
col1, col2, col3 = str_web.columns(3)

common_ai_config = types.GenerateContentConfig(
    temperature=0.7,
    system_instruction=f"You are a local Japan travel expert. Give outputs in clear, easy short bullet points. Language: {current_lang}.",
)

with col1:
    if str_web.button(tx["train_btn"], use_container_width=True):
        if not (prefecture and city):
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("Searching..."):
                prompt = f"Provide a guide on how to travel by train/subway in {city}, {prefecture}. Include major station names and IC card tips."
                res = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt, config=common_ai_config
                )
                str_web.info(res.text)

with col2:
    if str_web.button(tx["food_btn"], use_container_width=True):
        if not (prefecture and city):
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("Searching..."):
                prompt = f"List 3 must-try local foods or famous food areas in {city}, {prefecture} for tourists."
                res = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt, config=common_ai_config
                )
                str_web.success(res.text)

with col3:
    if str_web.button(tx["hotel_btn"], use_container_width=True):
        if not (prefecture and city):
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("Searching..."):
                prompt = f"Recommend the best areas to stay/book hotels in {city}, {prefecture} based on convenience and budget."
                res = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt, config=common_ai_config
                )
                str_web.warning(res.text)

# ----------------------------------------------------------------------
# --- MAPS INTEGRATION ---
if prefecture and city:
    str_web.markdown("<br>", unsafe_allow_html=True)
    search_query = (
        city.replace("区", "").replace("市", "") + f"+{prefecture.split(' ')[0]}"
    )
    map_url = f"https://maps.google.com/maps?q={search_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"
    str_web.markdown(
        f'<iframe src="{map_url}" width="100%" height="180" style="border:0; border-radius:10px;"></iframe>',
        unsafe_allow_html=True,
    )

# --- SECTION 4: TRIP ACTIVITIES & EXPANDERS ---
str_web.markdown("---")
str_web.subheader(tx["sec_trip"])

activity_mapping = {
    "English": [
        "Shopping at local supermarkets & home cooking experience",
        "Sento/Onsen etiquette & correct bathing method",
        "How to ride local buses and pay the fare correctly",
    ],
    "Myanmar": [
        "ဒေသတွင်းစူပါမားကတ်တွင် ဈေးဝယ်ခြင်းနှင့် အိမ်ချက်ချက်ပြုတ်မှု အတွေ့အကြုံ",
        "အများသုံးရေချိုးခန်း (Sento/Onsen) စည်းကမ်းနှင့် စနစ်တကျ ရေချိုးနည်း",
        "ဒေသန္တရဘတ်စ်ကားများ စနစ်တကျစီးနင်းခြင်းနှင့် ကားခပေးချေနည်း",
    ],
    "Japanese": [
        "地元のスーパーでの買い物と家庭料理の体験",
        "銭湯・温泉のマナーと正しい入浴方法",
        "ローカルバスの正しい乗り方と運賃の支払い方",
    ],
}

experience_type = str_web.selectbox(
    tx["act_label"],
    activity_mapping[current_lang],
    index=None,
    placeholder=tx["act_holder"],
)

# Expanders
with str_web.expander(tx["guide_box"]):
    if str_web.button(tx["guide_btn"], key="main_guide"):
        if prefecture and city and experience_type:
            with str_web.spinner("Loading..."):
                prompt = f"Provide local etiquette guide for '{experience_type}' in {city}, {prefecture}."
                res = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt, config=common_ai_config
                )
                str_web.markdown(res.text)
        else:
            str_web.error("⚠️ Please select all options first!")

with str_web.expander(tx["weather_box"]):
    if str_web.button(tx["weather_btn"], key="main_weather"):
        if prefecture and city:
            with str_web.spinner("Loading..."):
                prompt = f"Provide 2026 current month weather statistics for {city}, {prefecture} and clothing guide."
                res = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt, config=common_ai_config
                )
                str_web.markdown(res.text)
        else:
            str_web.error(tx["error_select"])

with str_web.expander(tx["calc_box"]):
    currency_target = str_web.selectbox(
        "Target Currency", ["MMK (Myanmar Kyat)", "USD (US Dollar)"]
    )
    yen_amount = str_web.number_input(
        "Amount in JPY", min_value=0, value=1000, step=500
    )
    if str_web.button(tx["calc_btn"], key="main_calc"):
        with str_web.spinner("Calculating..."):
            prompt = f"Convert {yen_amount} JPY to {currency_target} using realistic 2026 rates."
            res = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt, config=common_ai_config
            )
            str_web.markdown(res.text)

with str_web.expander(tx["sos_box"]):
    if str_web.button(tx["sos_btn"], key="main_sos"):
        with str_web.spinner("Loading..."):
            prompt = f"Provide Japan emergency numbers and 1 hospital near {city if city else 'Tokyo'} supporting foreigners."
            res = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt, config=common_ai_config
            )
            str_web.markdown(res.text)
