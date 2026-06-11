import os
import json
import streamlit as str_web
from google import genai
from google.genai import types
from PIL import Image

# 1. Page Config
str_web.set_page_config(page_title="TabiNavi Concierge", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced Custom CSS (UI/UX ပိုမိုကောင်းမွန်အောင် ပြင်ဆင်ထားသော စတိုင်များ)
str_web.markdown("""
<style>
    /* Premium Header Card */
    .custom-header {
        background: linear-gradient(135deg, #0F3A40 0%, #1D5B66 100%) !important;
        padding: 24px 20px !important;
        border-radius: 12px !important;
        text-align: center !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    /* Typography Hierarchy ကို ပိုမိုထင်ရှားစေခြင်း */
    .custom-header h1 {
        font-size: 32px !important; 
        font-weight: 800 !important;
        color: #FFFFFF !important;
        margin: 0 !important;
        letter-spacing: 0.5px !important;
    }
    .subtitle-text {
        color: #CBD5E1 !important;
        font-size: 14px !important;
        margin-top: 8px !important;
        font-weight: 400 !important;
    }

    /* Streamlit Button ကို Premium Card Style ပြောင်းလဲခြင်း + Hover Effect အသစ် */
    div.stButton > button {
        background-color: #1A202C !important;
        color: #FFFFFF !important;
        border: 1px solid #2D3748 !important;
        border-radius: 12px !important;
        padding: 20px 10px !important;
        min-height: 110px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        white-space: pre-line !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }
    /* Hover လုပ်လိုက်လျှင် သိသိသာသာ ပြောင်းလဲသွားမည့် အရောင်နှင့် ပုံစံ */
    div.stButton > button:hover {
        border-color: #4FD1C5 !important;
        background-color: #2D3748 !important;
        color: #4FD1C5 !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 6px 12px rgba(79, 209, 197, 0.2) !important;
    }
    div.stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* Map Corner Area ကို ကတ်ပြားများနှင့် တစ်သားတည်းဖြစ်အောင် ညှိခြင်း */
    .map-wrapper iframe {
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
    }

    /* Utility Row Widgets Layout */
    .utility-flex {
        display: flex !important;
        gap: 12px !important;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
    }
    .mini-card {
        flex: 1 !important;
        background-color: #1A202C !important;
        border: 1px solid #2D3748 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        text-align: center !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    .mini-card-title {
        font-size: 11px !important;
        color: #A0AEC0 !important;
        text-transform: uppercase !important;
        margin-bottom: 4px;
    }
    .mini-card-value {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "bookmarks" not in str_web.session_state:
    str_web.session_state.bookmarks = []
if "expenses" not in str_web.session_state:
    str_web.session_state.expenses = []
if "show_picker" not in str_web.session_state:
    str_web.session_state.show_picker = False

# Translations Dictionary
ui_translations = {
    "English": {
        "title": "TabiNavi Concierge", "sub": "Your Next-Gen AI Travel Companion",
        "pref_label": "Select Prefecture", "pref_holder": "Choose a prefecture...",
        "city_label": "Select City / Area", "city_holder": "Choose a city...",
        "sec_quick": "Quick Travel Services",
        "train_btn": "Routes Guide", "food_btn": "Food & Dining", "hotel_btn": "Hotels", "itinerary_btn": "6 Days Plan",
        "cam_box": "Smart Camera Translator", "cam_upload": "Upload image...",
        "text_box": "Text/Speech Translator", "text_input": "Enter text...",
        "sec_utilities": "Travel Utilities", "safety_box": "Disaster Safety Guide", "safety_btn": "Get Emergency Guide",
        "expense_box": "Travel Expense Tracker", "bookmark_box": "Saved Locations",
        "sec_trip": "Trip Activities & Local Etiquette", "act_label": "Select Activity Type", "act_holder": "Choose an activity...",
        "guide_btn": "Generate Guide", "weather_box": "Weather & Clothing Guide", "weather_btn": "Check Weather",
        "calc_box": "Currency Converter", "calc_btn": "Calculate", "sos_btn": "Show Emergency Contacts",
        "sidebar_title": "Control Panel",
    },
    "Myanmar": {
        "title": "TabiNavi Concierge", "sub": "အဆင့်မြင့် AI စနစ်သုံး အိတ်ဆောင်ခရီးသွားလမ်းညွှန်",
        "pref_label": "ပြည်နယ်/ခရိုင် ကို ရွေးချယ်ပါ", "pref_holder": "ခရိုင်တစ်ခု ရွေးချယ်ပေးပါ...",
        "city_label": "မြို/ဒေသ ကို ရွေးချယ်ပါ", "city_holder": "မြို့ကို ရွေးချယ်ပေးပါ...",
        "sec_quick": "အမြန်အသုံးပြုနိုင်မည့် ဝန်ဆောင်မှုများ",
        "train_btn": "ရထားလမ်းကြောင်း", "food_btn": "အစားအသောက်ဆိုင်", "hotel_btn": "ဟိုတယ်တည်းခိုခန်း", "itinerary_btn": "ခရီးစဉ်အကြံပြုချက်",
        "cam_box": "Smart ကင်မရာ ဘာသာပြန်စနစ်", "cam_upload": "ပုံရိပ် တင်ပေးပါ...",
        "text_box": "အချိန်နဲ့တပြေးညီ ဘာသာပြန်", "text_input": "စာသားရိုက်ပါ...",
        "sec_utilities": "ခရီးသွား အသုံးဆောင်များနှင့် စာရင်းများ", "safety_box": "သဘာဝဘေးအန္တရာယ် ဘေးကင်းလုံခြုံရေး", "safety_btn": "အရေးပေါ် လမ်းညွှန်ချက်ရယူမည်",
        "expense_box": "ခရီးသွားစရိတ် မှတ်တမ်း", "bookmark_box": "မှတ်သားထားသော နေရာများ",
        "sec_trip": "ပြုလုပ်မည့် အတွေ့အကြုံများနှင့် စည်းကမ်းများ", "act_label": "လုပ်ဆောင်မည့် အတွေ့အကြုံ အမျိုးအစား", "act_holder": "အတွေ့အကြုံ ရွေးချယ်ရန်...",
        "guide_btn": "လမ်းညွှန်ချက် ထုတ်လုပ်မည်", "weather_box": "ရာသီဥတုနှင့် ဝတ်စားဆင်ယင်မှု လမ်းညွှန်", "weather_btn": "ရာသီဥတု စစ်မည်",
        "calc_box": "ငွေလဲနှုန်း တွက်ချက်စနစ်", "calc_btn": "ငွေလဲနှုန်း တွက်မည်", "sos_btn": "အရေးပေါ် အချက်အလက်ပြပါ",
        "sidebar_title": "ထိန်းချုပ်ရေးခန်း",
    },
    "Japanese": {
        "title": "TabiNavi Concierge", "sub": "次世代AI旅行コンパニオン",
        "pref_label": "都道府県を選択", "pref_holder": "都道府県 を選択してください...",
        "city_label": "市区町村を選択", "city_holder": "市区町村 を選択してください...",
        "sec_quick": "クイック旅行サービス",
        "train_btn": "電車の乗換案内", "food_btn": "グルメ・周辺の飲食店", "hotel_btn": "おすすめの宿泊エリア", "itinerary_btn": "おすすめプラン",
        "cam_box": "スマートカメラ翻訳", "cam_upload": "画像をアップロード...",
        "text_box": "リアルタイム翻訳", "text_input": "テキストを入力...",
        "sec_utilities": "旅行ユーティリティ", "safety_box": "災害・防災ガイド", "safety_btn": "避難案内を取得",
        "expense_box": "旅費の家計簿", "bookmark_box": "お気に入り保存場所",
        "sec_trip": "アクティビティ & マナーガイド", "act_label": "アクティビティの種類を選択", "act_holder": "アクティビティを選択...",
        "guide_btn": "ガイドを生成", "weather_box": "天気・服装ガイド", "weather_btn": "天気をチェック",
        "calc_box": "通貨換算ツール", "calc_btn": "換算する", "sos_btn": "緊急情報を表示",
        "sidebar_title": "コントロールパネル",
    },
}

# --- SIDEBAR TOOLS ---
with str_web.sidebar:
    str_web.markdown(f"### ⚙️ {ui_translations['English']['sidebar_title']}")
    language_options = {"🇺🇸 English": "English", "🇲🇲 Myanmar (မြန်မာ)": "Myanmar", "🇯🇵 Japanese": "Japanese"}
    selected_lang_label = str_web.selectbox("🌐 Language", list(language_options.keys()), index=0)
    current_lang = language_options[selected_lang_label]
    tx = ui_translations[current_lang]

    str_web.markdown("---")
    with str_web.expander(tx["cam_box"]):
        uploaded_file = str_web.file_uploader(tx["cam_upload"], type=["jpg", "jpeg", "png"])
        if uploaded_file and str_web.button("🔍 Translate Image", use_container_width=True):
            client = genai.Client(api_key=str_web.secrets.get("GEMINI_API_KEY"))
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=[f"Translate into {current_lang}:", Image.open(uploaded_file)]):
                full_text += chunk.text
                placeholder.markdown(full_text)

    with str_web.expander(tx["text_box"]):
        input_text = str_web.text_input(tx["text_input"], key="side_txt_in")
        if str_web.button("🌐 Translate Text", use_container_width=True) and input_text:
            client = genai.Client(api_key=str_web.secrets.get("GEMINI_API_KEY"))
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"Translate into Japanese with Romaji: '{input_text}'"):
                full_text += chunk.text
                placeholder.markdown(full_text)

# --- CORE ENGINE SETUP ---
client = genai.Client(api_key=str_web.secrets.get("GEMINI_API_KEY"))
prefecture_city_map = {}
if os.path.exists("japan_data.json"):
    with open("japan_data.json", "r", encoding="utf-8") as f:
        prefecture_city_map = json.load(f)

# Top Premium Title Banner
str_web.markdown(f'''
<div class="custom-header">
    <h1>{tx["title"]}</h1>
    <p class="subtitle-text">{tx["sub"]}</p>
</div>
''', unsafe_allow_html=True)

# Select Filter Area
col_pref, col_city = str_web.columns(2)
with col_pref:
    prefecture = str_web.selectbox(tx["pref_label"], list(prefecture_city_map.keys()) if prefecture_city_map else [], index=None, placeholder=tx["pref_holder"])
with col_city:
    city = str_web.selectbox(tx["city_label"], prefecture_city_map.get(prefecture, []) if prefecture else [], index=None, placeholder=tx["city_holder"], disabled=not prefecture)

common_ai_config = types.GenerateContentConfig(temperature=0.7, system_instruction=f"Respond using concise, short bullet points. Output language: {current_lang}.")

# --- USER VIEW INTERACTION ---
if prefecture and city:
    loc_context = f"{city}, {prefecture}"
    str_web.markdown(f"### {tx['sec_quick']}")
    
    grid_col1, grid_col2, grid_col3, grid_col4 = str_web.columns(4)
    
    with grid_col1:
        if str_web.button(f"🚄\n\n{tx['train_btn']}", use_container_width=True, key="btn_train_main"):
            with str_web.spinner("Loading..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"Provide train route guide for {loc_context}.", config=common_ai_config):
                    full_text += chunk.text
                    placeholder.info(full_text)

    with grid_col2:
        if str_web.button(f"🍱\n\n{tx['food_btn']}", use_container_width=True, key="btn_food_main"):
            with str_web.spinner("Loading..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"List 3 famous food spots in {loc_context}.", config=common_ai_config):
                    full_text += chunk.text
                    placeholder.success(full_text)

    with grid_col3:
        if str_web.button(f"🏨\n\n{tx['hotel_btn']}", use_container_width=True, key="btn_hotel_main"):
            with str_web.spinner("Loading..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"Recommend best hotel stay areas in {loc_context}.", config=common_ai_config):
                    full_text += chunk.text
                    placeholder.warning(full_text)

    with grid_col4:
        if str_web.button(f"🌸\n\n{tx['itinerary_btn']}", use_container_width=True, key="btn_plan_main"):
            str_web.session_state.show_picker = True

    # ရက်ရွေးချယ်မှု စနစ်
    if str_web.session_state.show_picker:
        options_map = {
            "English": ["1 Day", "2 Days", "3 Days", "4 Days", "5 Days", "6 Days", "7 Days"],
            "Myanmar": ["1 ရက်စာ", "2 ရက်စာ", "3 ရက်စာ", "4 ရက်စာ", "5 ရက်စာ", "6 ရက်စာ", "7 ရက်စာ"],
            "Japanese": ["1日間", "2日間", "3日間", "4日間", "5日間", "6日間", "7日間"]
        }
        selected_days = str_web.selectbox("Select Duration", options_map.get(current_lang, options_map["English"]))
        if str_web.button("🚀 Confirm & Generate", use_container_width=True):
            with str_web.spinner("Loading..."):
                days_number = "".join(filter(str.isdigit, selected_days))
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"Create {days_number}-day itinerary for {loc_context}.", config=common_ai_config):
                    full_text += chunk.text
                    placeholder.markdown(full_text)
            str_web.session_state.show_picker = False

    st_bookmark = str_web.button(f"⭐ Save {city} to Bookmarks", use_container_width=True)
    if st_bookmark:
        bookmark_item = f"{city} ({prefecture})"
        if bookmark_item not in str_web.session_state.bookmarks:
            str_web.session_state.bookmarks.append(bookmark_item)
            str_web.toast(f"Saved {city}!")

    # 🛠️ Google Map Embed Link ပြင်ဆင်ချက် (URL အမှားနှင့် Query စနစ်ကို ပိုမှန်အောင် ညှိထားသည်)
    search_query = city.replace("区", "").replace("市", "") + f", {prefecture}"
    map_url = f"https://maps.google.com/maps?q={search_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"
    str_web.markdown(f'<div class="map-wrapper"><iframe src="{map_url}" width="100%" height="280" style="border:0;"></iframe></div>', unsafe_allow_html=True)

    # --- Etiquette Panel ---
    str_web.markdown("---")
    str_web.markdown(f"### {tx['sec_trip']}")
    activity_mapping = {
        "English": ["Shopping at supermarkets & cooking", "Sento/Onsen etiquette & bathing", "Riding local buses and fares", "Visiting shrines and temples"],
        "Myanmar": ["ဒေသတွင်းစူပါမားကတ်တွင် ဈေးဝယ်ခြင်း", "အများသုံးရေချိုးခန်း (Onsen) စည်းကမ်းများ", "ဒေသန္တရဘတ်စ်ကားများ စီးနင်းခြင်း", "ဘုရားကျောင်းများနှင့် နတ်ကွန်းများသို့ လည်ပတ်ခြင်း"],
        "Japanese": ["スーパーでの買い物と自炊", "銭湯・温泉の入浴マナー", "路線バスの利用方法と運賃", "神社・仏閣の参拝マナー"]
    }
    experience_type = str_web.selectbox(tx["act_label"], activity_mapping.get(current_lang, activity_mapping["English"]), index=None, placeholder=tx["act_holder"])
    if experience_type and str_web.button(tx["guide_btn"], use_container_width=True):
        with str_web.spinner("Generating..."):
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"Provide etiquette guide for '{experience_type}' in {loc_context}.", config=common_ai_config):
                full_text += chunk.text
                placeholder.markdown(full_text)

    # --- Utilities Weather & Currency Cards ---
    str_web.markdown("---")
    str_web.markdown('''
    <div class="utility-flex">
        <div class="mini-card"><div class="mini-card-title">🌤️ Weather</div><div class="mini-card-value">⛅ 15°C</div></div>
        <div class="mini-card"><div class="mini-card-title">💱 Currency</div><div class="mini-card-value">🇺🇸 1$ = 154¥ 🇯🇵</div></div>
    </div>
    ''', unsafe_allow_html=True)
    
    col_w, col_c = str_web.columns(2)
    with col_w:
        if str_web.button(tx["weather_btn"], use_container_width=True, key="w_btn"):
            with str_web.spinner("Loading..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"Provide current month weather for {loc_context}.", config=common_ai_config):
                    full_text += chunk.text
                    placeholder.markdown(full_text)
    with col_c:
        yen_amount = str_web.number_input("Amount in JPY", min_value=0, value=1000, step=500)
        if str_web.button(tx["calc_btn"], use_container_width=True, key="c_btn"):
            with str_web.spinner("Calculating..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"Convert {yen_amount} JPY to MMK/USD with recent rates.", config=common_ai_config):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    # --- Lower Tabs Area ---
    str_web.markdown("---")
    str_web.markdown(f"### {tx['sec_utilities']}")
    tab_safety, tab_expense, tab_bookmarks = str_web.tabs([tx["safety_box"], tx["expense_box"], tx["bookmark_box"]])

    with tab_safety:
        if str_web.button(tx["safety_btn"], use_container_width=True):
            with str_web.spinner("Loading..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=f"Provide disaster evacuation tips for tourists in {city}.", config=common_ai_config):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    with tab_expense:
        exp_name = str_web.text_input("Expense Item", placeholder="Ramen")
        exp_amt = str_web.number_input("Amount (JPY)", min_value=0, step=100, key="exp_num_input")
        if str_web.button("➕ Add Expense", use_container_width=True) and exp_name and exp_amt > 0:
            str_web.session_state.expenses.append({"item": exp_name, "cost": exp_amt})
        if str_web.session_state.expenses:
            str_web.markdown(f"Total Spent: **{sum(item['cost'] for item in str_web.session_state.expenses):,} JPY**")

    with tab_bookmarks:
        if str_web.session_state.bookmarks:
            for mark in str_web.session_state.bookmarks:
                str_web.markdown(f"📌 {mark}")
        else:
            str_web.caption("No saved locations yet.")
else:
    str_web.info("💡 Please select both Prefecture and City above to unlock travel assistance tools.")