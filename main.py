import os
import json
import streamlit as str_web
from google import genai
from google.genai import types
from PIL import Image

# 🎨 Streamlit Configuration (Clean & Modern Layout)
str_web.set_page_config(page_title="TabiNavi", layout="centered")

# Initialize Session States
if "bookmarks" not in str_web.session_state:
    str_web.session_state.bookmarks = []
if "expenses" not in str_web.session_state:
    str_web.session_state.expenses = []

# --- 🌐 MULTI-LANGUAGE DICTIONARY (Premium Branding Applied) ---
ui_translations = {
    "English": {
        "title": "TabiNavi",
        "sub": "Your Next-Gen AI Travel Companion",
        "pref_label": "Select Prefecture",
        "pref_holder": "Choose a prefecture...",
        "city_label": "Select City / Area",
        "city_holder": "Choose a city...",
        "sec_quick": "Quick Travel Services",
        "train_btn": "Train & Routes",
        "food_btn": "Food & Dining",
        "hotel_btn": "Hotel Booking",
        "itinerary_btn": "3-Day Planner",
        "sec_ai_tools": "✨ TabiNavi Concierge",
        "cam_box": "Smart Camera Translator",
        "cam_upload": "Upload menu or signboard image...",
        "text_box": "Text/Speech Translator",
        "text_input": "Enter text to translate...",
        "sec_utilities": "Travel Utilities",
        "safety_box": "Disaster Safety Guide",
        "safety_btn": "Get Emergency Guide",
        "expense_box": "Travel Expense Tracker",
        "bookmark_box": "Saved Locations",
        "sec_trip": "Trip Activities & Local Etiquette",
        "act_label": "Select Activity Type",
        "act_holder": "Choose an activity...",
        "guide_box": "Local Etiquette Guide",
        "guide_btn": "Generate Guide",
        "weather_box": "Weather & Clothing Guide",
        "weather_btn": "Check Weather",
        "calc_box": "Currency Converter",
        "calc_btn": "Calculate",
        "sos_box": "Emergency SOS & Hospitals",
        "sos_btn": "Show Emergency Contacts",
        "sidebar_title": "Control Panel",
    },
    "Myanmar": {
        "title": "TabiNavi",
        "sub": "အဆင့်မြင့် AI စနစ်သုံး အိတ်ဆောင်ခရီးသွားလမ်းညွှန်",
        "pref_label": "ပြည်နယ်/ခရိုင် ကို ရွေးချယ်ပါ",
        "pref_holder": "ခရိုင်တစ်ခု ရွေးချယ်ပေးပါ...",
        "city_label": "မြို/ဒေသ ကို ရွေးချယ်ပါ",
        "city_holder": "မြို့ကို ရွေးချယ်ပေးပါ...",
        "sec_quick": "အမြန်အသုံးပြုနိုင်မည့် ဝန်ဆောင်မှုများ",
        "train_btn": "ရထားလမ်းကြောင်း",
        "food_btn": "အစားအသောက်ဆိုင်",
        "hotel_btn": "ဟိုတယ်တည်းခိုခန်း",
        "itinerary_btn": "၃ ရက်စာ ခရီးစဉ်",
        "sec_ai_tools": "✨ TabiNavi စမတ်ဝန်ဆောင်မှု",
        "cam_box": "Smart ကင်မရာ ဘာသာပြန်စနစ်",
        "cam_upload": "မီနူး သို့မဟုတ် ဆိုင်းဘုတ်ပုံရိပ် တင်ပေးပါ...",
        "text_box": "အချိန်နဲ့တပြေးညီ ဘာသာပြန်",
        "text_input": "ဘာသာပြန်လိုသည့် စာသားရိုက်ပါ...",
        "sec_utilities": "ခရီးသွား အသုံးဆောင်များနှင့် စာရင်းများ",
        "safety_box": "သဘာဝဘေးအန္တရာယ် ဘေးကင်းလုံခြုံရေး လမ်းညွှန်",
        "safety_btn": "အရေးပေါ် လမ်းညွှန်ချက်ရယူမည်",
        "expense_box": "ခရီးသွားစရိတ် မှတ်တမ်း",
        "bookmark_box": "မှတ်သားထားသော နေရာများ",
        "sec_trip": "ပြုလုပ်မည့် အတွေ့အကြုံများနှင့် စည်းကမ်းများ",
        "act_label": "လုပ်ဆောင်မည့် အတွေ့အကြုံ အမျိုးအစား",
        "act_holder": "အတွေ့အကြုံ ရွေးချယ်ရန်...",
        "guide_box": "ဒေသတွင်း စည်းကမ်းနှင့် လမ်းညွှန်ချက်",
        "guide_btn": "လမ်းညွှန်ချက် ထုတ်လုပ်မည်",
        "weather_box": "ရာသီဥတုနှင့် ဝတ်စားဆင်ယင်မှု လမ်းညွှန်",
        "weather_btn": "ရာသီဥတု စစ်မည်",
        "calc_box": "ငွေလဲနှုန်း တွက်ချက်စနစ်",
        "calc_btn": "ငွေလဲနှုန်း တွက်မည်",
        "sos_box": "အရေးပေါ် ဖုန်းနံပါတ်များနှင့် ဆေးရုံများ",
        "sos_btn": "အရေးပေါ် အချက်အလက်ပြပါ",
        "sidebar_title": "ထိန်းချုပ်ရေးခန်း",
    },
    "Japanese": {
        "title": "TabiNavi",
        "sub": "次世代AI旅行コンパニオン",
        "pref_label": "都道府県を選択",
        "pref_holder": "都道府県 を選択してください...",
        "city_label": "市区町村を選択",
        "city_holder": "市区町村 を選択してください...",
        "sec_quick": "クイック旅行サービス",
        "train_btn": "電車の乗換案内",
        "food_btn": "グルメ・周辺の飲食店",
        "hotel_btn": "おすすめの宿泊エリア",
        "itinerary_btn": "3日間おすすめプラン",
        "sec_ai_tools": "✨ TabiNaviコンシェルジュ",
        "cam_box": "スマートカメラ翻訳",
        "cam_upload": "メニューや看板の画像をアップロード...",
        "text_box": "リアルタイム翻訳",
        "text_input": "翻訳するテキストを入力...",
        "sec_utilities": "旅行ユーティリティ",
        "safety_box": "災害・防災ガイド",
        "safety_btn": "避難案内を取得",
        "expense_box": "旅費の家計簿",
        "bookmark_box": "お気に入り保存場所",
        "sec_trip": "アクティビティ & マナーガイド",
        "act_label": "アクティビティの種類を選択",
        "act_holder": "アクティビティを選択...",
        "guide_box": "ローカルマナーガイド",
        "guide_btn": "ガイドを生成",
        "weather_box": "天気・服装ガイド",
        "weather_btn": "天気をチェック",
        "calc_box": "通貨換算ツール",
        "calc_btn": "換算する",
        "sos_box": "緊急連絡先 & 病院案内",
        "sos_btn": "緊急情報を表示",
        "sidebar_title": "コントロールパネル",
    },
}

# --- ⚙️ SIDEBAR SETUP ---
with str_web.sidebar:
    str_web.markdown(f"### ⚙️ {ui_translations['English']['sidebar_title']}")
    language_options = {
        "🇺🇸 English": "English",
        "🇲🇲 Myanmar (မြန်မာ)": "Myanmar",
        "🇯🇵 Japanese": "Japanese",
    }
    selected_lang_label = str_web.selectbox(
        "🌐 Language", list(language_options.keys()), index=0
    )
    current_lang = language_options[selected_lang_label]
    tx = ui_translations[current_lang]

    str_web.markdown("---")
    str_web.markdown(f"### {tx['sec_ai_tools']}")

    # 📸 Smart Camera Translator (Sidebar Inside)
    with str_web.expander(tx["cam_box"]):
        uploaded_file = str_web.file_uploader(
            tx["cam_upload"], type=["jpg", "jpeg", "png"]
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            str_web.image(
                image,
                caption="Uploaded Image",
                use_container_width=True,
            )
            if str_web.button("🔍 Translate Image", use_container_width=True):
                api_key = str_web.secrets.get("GEMINI_API_KEY")
                if api_key:
                    client = genai.Client(api_key=api_key)
                    placeholder = str_web.empty()
                    full_text = ""
                    for chunk in client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=[f"Translate into {current_lang}:", image],
                    ):
                        full_text += chunk.text
                        placeholder.markdown(full_text)

    # 🗣️ Text Translator (Sidebar Inside)
    with str_web.expander(tx["text_box"]):
        input_text = str_web.text_input(tx["text_input"], key="side_txt_in")
        if str_web.button("🌐 Translate", use_container_width=True):
            api_key = str_web.secrets.get("GEMINI_API_KEY")
            if input_text and api_key:
                client = genai.Client(api_key=api_key)
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=(f"Translate into Japanese with Romaji: '{input_text}'"),
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

# --- API CLIENT & DATA SETUP ---
api_key = str_web.secrets.get("GEMINI_API_KEY")
if not api_key:
    str_web.error("GEMINI_API_KEY Missing!")
    str_web.stop()
client = genai.Client(api_key=api_key)

prefecture_city_map = {}
if os.path.exists("japan_data.json"):
    with open("japan_data.json", "r", encoding="utf-8") as f:
        prefecture_city_map = json.load(f)

# --- MAIN SCREEN DISPLAY ---
str_web.title(tx["title"])
str_web.caption(tx["sub"])

# Location Filters
col_pref, col_city = str_web.columns(2)
with col_pref:
    prefecture = str_web.selectbox(
        tx["pref_label"],
        list(prefecture_city_map.keys()) if prefecture_city_map else [],
        index=None,
        placeholder=tx["pref_holder"],
    )

with col_city:
    if prefecture:
        city = str_web.selectbox(
            tx["city_label"],
            prefecture_city_map.get(prefecture, []),
            index=None,
            placeholder=tx["city_holder"],
        )
    else:
        city = str_web.selectbox(
            tx["city_label"],
            [],
            index=None,
            placeholder="Select prefecture first",
            disabled=True,
        )

common_ai_config = types.GenerateContentConfig(
    temperature=0.7,
    system_instruction=(
        "Respond using concise, short bullet points. "
        f"Output language: {current_lang}."
    ),
)

# --- CONDITIONAL VISIBILITY ---
if not (prefecture and city):
    str_web.markdown("---")
    str_web.info(
        "💡 Please select both Prefecture and City above to unlock "
        "travel assistance tools."
    )
else:
    loc_context = f"{city}, {prefecture}"

    # Quick Travel Services Section
    str_web.markdown("---")
    str_web.subheader(tx["sec_quick"])

    row1_col1, row1_col2 = str_web.columns(2)
    with row1_col1:
        if str_web.button(tx["train_btn"], use_container_width=True):
            with str_web.spinner("Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Provide train route guide for {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.info(full_text)

    with row1_col2:
        if str_web.button(tx["food_btn"], use_container_width=True):
            with str_web.spinner("Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"List 3 famous food spots in {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.success(full_text)

    row2_col1, row2_col2 = str_web.columns(2)
    with row2_col1:
        if str_web.button(tx["hotel_btn"], use_container_width=True):
            with str_web.spinner("Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=(f"Recommend best hotel stay areas in {loc_context}."),
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.warning(full_text)

    with row2_col2:
        if str_web.button(tx["itinerary_btn"], use_container_width=True):
            with str_web.spinner("Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Create 3-day itinerary for {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    # Bookmark Action Bar
    if str_web.button(f"📌 Save {city} to Bookmarks", use_container_width=True):
        bookmark_item = f"{city} ({prefecture})"
        if bookmark_item not in str_web.session_state.bookmarks:
            str_web.session_state.bookmarks.append(bookmark_item)
            str_web.toast(f"Saved {city}!")

    # Maps Integration
    search_query = (
        city.replace("区", "").replace("市", "") + f"+{prefecture.split(' ')[0]}"
    )
    map_url = (
        "https://maps.google.com/maps?"
        f"q={search_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"
    )
    str_web.markdown(
        (
            f'<iframe src="{map_url}" width="100%" height="200" '
            'style="border:0; border-radius:12px;"></iframe>'
        ),
        unsafe_allow_html=True,
    )

    # Currency & Weather Section
    str_web.markdown("---")
    col_w, col_c = str_web.columns(2)

    with col_w:
        str_web.markdown(f"##### 🌤️ {tx['weather_box']}")
        if str_web.button(tx["weather_btn"], use_container_width=True):
            with str_web.spinner("Loading..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=(
                        "Provide 2026 current month weather and clothing "
                        f"for {loc_context}."
                    ),
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    with col_c:
        str_web.markdown(f"##### 💱 {tx['calc_box']}")
        yen_amount = str_web.number_input(
            "Amount in JPY",
            min_value=0,
            value=1000,
            step=500,
            label_visibility="collapsed",
        )
        if str_web.button(tx["calc_btn"], use_container_width=True):
            with str_web.spinner("Calculating..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=(f"Convert {yen_amount} JPY to MMK/USD with 2026 rates."),
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    # Activities & Etiquette Section
    str_web.markdown("---")
    str_web.subheader(tx["sec_trip"])

    activity_mapping = {
        "English": [
            "Shopping at supermarkets & cooking",
            "Sento/Onsen etiquette & bathing",
            "Riding local buses and fares",
            "Visiting shrines and temples",
            "Shinkansen & train transit manners",
            "Dining at traditional restaurants",
            "Garbage disposal & recycling rules",
            "Staying at Ryokan heritage inns",
            "Smartphone & photo taking etiquette"
        ],
        "Myanmar": [
            ("ဒေသတွင်းစူပါမားကတ်တွင် ဈေးဝယ်ခြင်း၊"),
            ("အများသုံးရေချိုးခန်း (Onsen) စည်းကမ်းများ၊"),
            ("ဒေသန္တရဘတ်စ်ကားများ စီးနင်းခြင်း၊"),
            ("ဘုရားကျောင်းများနှင့် နတ်ကွန်းများသို့ လည်ပတ်ခြင်း၊"),
            ("ကျည်ဆန်ရထားနှင့် အများပြည်သူသုံး ရထားစီးခြင်း၊"),
            ("ဂျပန်ရိုးရာ စားသောက်ဆိုင်များတွင် စားသောက်ခြင်း、"),
            ("စနစ်ကျသော အမှိုက်စွန့်ပစ်ခြင်းနှင့် ပြန်လည်အသုံးပြုခြင်း၊"),
            ("ရိုးရာတည်းခိုခန်း (Ryokan) များတွင် တည်းခိုခြင်း၊"),
            ("စမတ်ဖုန်းနှင့် ကင်မရာအသုံးပြုမှု ယဉ်ကျေးမှုများ")
        ],
        "Japanese": [
            "スーパーでの買い物と自炊",
            "銭湯・温泉の入浴マナー",
            "路線バスの利用方法と運賃",
            "神社・仏閣の参拝マナー",
            "新幹線・電車の乗車マナー",
            "伝統的な飲食店でのマナー",
            "ゴミの分別・リサイクルのルール",
            "伝統旅館での宿泊マナー",
            "スマホ利用・写真撮影のマナー"
        ]
    }
    experience_type = str_web.selectbox(
        tx["act_label"],
        activity_mapping.get(current_lang, activity_mapping["English"]),
        index=None,
        placeholder=tx["act_holder"],
        label_visibility="collapsed",
    )

    if experience_type:
        if str_web.button(tx["guide_btn"], use_container_width=True):
            with str_web.spinner("Generating..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=(
                        f"Provide etiquette guide for '{experience_type}' "
                        f"in {loc_context}."
                    ),
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    # Utilities & Pro Utilities
    str_web.markdown("---")
    str_web.subheader(tx["sec_utilities"])

    tab_safety, tab_expense, tab_bookmarks = str_web.tabs(
        [tx["safety_box"], tx["expense_box"], tx["bookmark_box"]]
    )

    with tab_safety:
        col_sos, col_dis = str_web.columns(2)
        with col_sos:
            if str_web.button(tx["sos_btn"], use_container_width=True):
                with str_web.spinner("Loading..."):
                    placeholder = str_web.empty()
                    full_text = ""
                    for chunk in client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=(
                            "Provide Japan emergency numbers and 1 "
                            f"foreign-friendly hospital near {city}."
                        ),
                        config=common_ai_config,
                    ):
                        full_text += chunk.text
                        placeholder.markdown(full_text)
        with col_dis:
            if str_web.button(tx["safety_btn"], use_container_width=True):
                with str_web.spinner("Loading..."):
                    placeholder = str_web.empty()
                    full_text = ""
                    for chunk in client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=(
                            f"Provide disaster evacuation tips for tourists "
                            f"in {city}."
                        ),
                        config=common_ai_config,
                    ):
                        full_text += chunk.text
                        placeholder.markdown(full_text)

    with tab_expense:
        col_item, col_cost = str_web.columns([2, 1])
        with col_item:
            exp_name = str_web.text_input(
                "Expense Item",
                placeholder="e.g., Ramen dinner",
                label_visibility="collapsed",
            )
        with col_cost:
            exp_amt = str_web.number_input(
                "Amount (JPY)",
                min_value=0,
                step=100,
                label_visibility="collapsed",
            )
        if str_web.button("➕ Add Expense", use_container_width=True):
            if exp_name and exp_amt > 0:
                str_web.session_state.expenses.append(
                    {"item": exp_name, "cost": exp_amt}
                )

        if str_web.session_state.expenses:
            total_spent = sum(item["cost"] for item in str_web.session_state.expenses)
            str_web.markdown(f"Total Spent: **{total_spent:,} JPY**")
            if str_web.button("🗑️ Clear Expenses"):
                str_web.session_state.expenses = []
                str_web.rerun()

    with tab_bookmarks:
        if str_web.session_state.bookmarks:
            for mark in str_web.session_state.bookmarks:
                str_web.markdown(f"📌 **{mark}**")
            if str_web.button("🗑️ Clear Bookmarks"):
                str_web.session_state.bookmarks = []
                str_web.rerun()
        else:
            str_web.caption("No saved locations yet.")
