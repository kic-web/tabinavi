import os
import json
import streamlit as str_web
from google import genai
from google.genai import types
from PIL import Image

# 🎨 Streamlit Configuration (Clean & Modern Layout)
str_web.set_page_config(page_title="TabiNavi Pro AI", layout="centered")

# Initialize Session States
if "bookmarks" not in str_web.session_state:
    str_web.session_state.bookmarks = []
if "expenses" not in str_web.session_state:
    str_web.session_state.expenses = []

# --- 🌐 MULTI-LANGUAGE DICTIONARY (Cleaned: Numbers & Excess Emojis Removed) ---
ui_translations = {
    "English": {
        "title": "TabiNavi Pro AI",
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
        "sec_ai_tools": "Advanced AI Tools",
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
        "title": "TabiNavi Pro AI",
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
        "sec_ai_tools": "အဆင့်မြင့် AI ကိရိယာများ",
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
}

# --- ⚙️ SIDEBAR SETUP (ရွှေ့ပြောင်းခြင်း) ---
# တစ်ခါတလေမှသုံးမယ့် Advanced AI Tools တွေကို Sidebar ထဲရွှေ့ပြီး Main Screen ကို ရှင်းထုတ်လိုက်ပါတယ်
with str_web.sidebar:
    str_web.markdown(f"### ⚙️ {ui_translations['English']['sidebar_title']}")
    language_options = {"🇺🇸 English": "English", "🇲🇲 Myanmar (မြန်မာ)": "Myanmar"}
    selected_lang_label = str_web.selectbox(
        "🌐 Language", list(language_options.keys()), index=0
    )
    current_lang = language_options[selected_lang_label]
    tx = ui_translations[current_lang]

    str_web.markdown("---")
    str_web.markdown(f"### 🧠 {tx['sec_ai_tools']}")

    # 📸 Smart Camera Translator (Sidebar Inside)
    with str_web.expander(tx["cam_box"]):
        uploaded_file = str_web.file_uploader(
            tx["cam_upload"], type=["jpg", "jpeg", "png"]
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            str_web.image(image, caption="Uploaded Image", use_container_width=True)
            if str_web.button("🔍 Translate Image", use_container_width=True):
                # Setup api client inside sidebar logic if triggered
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
                    contents=f"Translate into Japanese with Romaji: '{input_text}'",
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

# 1. Location Filters (Side-by-Side Columns for cleaner look)
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
    system_instruction=f"Respond using concise, short bullet points. Output language: {current_lang}.",
)

# ----------------------------------------------------------------------
# ⚡ CONDITIONAL VISIBILITY (Prefecture/City မရွေးရသေးရင် အောက်က Features တွေကို ဝှက်ထားပေးခြင်း)
# ----------------------------------------------------------------------
if not (prefecture and city):
    str_web.markdown("---")
    str_web.info(
        "💡 Please select both Prefecture and City above to unlock travel assistance tools."
    )
else:
    loc_context = f"{city}, {prefecture}"

    # 🚀 Quick Travel Services Section (2x2 Grid Layout with Full-Width Buttons)
    str_web.markdown("---")
    str_web.subheader(tx["sec_quick"])

    row1_col1, row1_col2 = str_web.columns(2)
    with row1_col1:
        if str_web.button(tx["train_btn"], use_container_width=True):
            with str_web.spinner("🧠 Connecting AI..."):
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
            with str_web.spinner("🧠 Connecting AI..."):
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
            with str_web.spinner("🧠 Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Recommend best hotel stay areas in {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.warning(full_text)

    with row2_col2:
        if str_web.button(tx["itinerary_btn"], use_container_width=True):
            with str_web.spinner("🧠 Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Create 3-day itinerary for {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    # 📌 Bookmark Action Bar
    if str_web.button(f"📌 Save {city} to Bookmarks", use_container_width=True):
        bookmark_item = f"{city} ({prefecture})"
        if bookmark_item not in str_web.session_state.bookmarks:
            str_web.session_state.bookmarks.append(bookmark_item)
            str_web.toast(f"Saved {city}!")

    # 🗺️ Maps Integration
    search_query = (
        city.replace("区", "").replace("市", "") + f"+{prefecture.split(' ')[0]}"
    )
    map_url = f"https://maps.google.com/maps?q={search_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"
    str_web.markdown(
        f'<iframe src="{map_url}" width="100%" height="200" style="border:0; border-radius:12px;"></iframe>',
        unsafe_allow_html=True,
    )

    # 🌤️ Currency & Weather Section (No Expanders - Exposed directly as requested)
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
                    contents=f"Provide 2026 current month weather and clothing for {loc_context}.",
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
                    contents=f"Convert {yen_amount} JPY to MMK/USD with 2026 rates.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    # 🎯 Activities & Etiquette Section
    str_web.markdown("---")
    str_web.subheader(tx["sec_trip"])

    activity_mapping = {
        "English": [
            "Shopping at supermarkets & cooking",
            "Sento/Onsen etiquette & bathing",
            "Riding local buses and fares",
        ],
        "Myanmar": [
            "ဒေသတွင်းစူပါမားကတ်တွင် ဈေးဝယ်ခြင်း",
            "အများသုံးရေချိုးခန်း (Onsen) စည်းကမ်းများ",
            "ဒေသန္တရဘတ်စ်ကားများ စီးနင်းခြင်း",
        ],
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
                    contents=f"Provide etiquette guide for '{experience_type}' in {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    # 🛡️ Utilities & Pro Utilities (Disaster, SOS, Expense, Bookmarks)
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
                        contents=f"Provide Japan emergency numbers and 1 foreign-friendly hospital near {city}.",
                        config=common_ai_config,
                    ):
                        full_text += chunk.text
                        placeholder.markdown(full_text)
        with col_dis:
            if str_web.button(tx["safety_btn"], use_container_width=True):
                with str_web.spinner("🚨 Loading..."):
                    placeholder = str_web.empty()
                    full_text = ""
                    for chunk in client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=f"Provide disaster evacuation tips for tourists in {city}.",
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
                "Amount (JPY)", min_value=0, step=100, label_visibility="collapsed"
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
