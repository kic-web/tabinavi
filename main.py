import os
import json
import streamlit as str_web
from google import genai
from google.genai import types
from PIL import Image

# 🎨 Streamlit Advanced Page Configuration
str_web.set_page_config(page_title="TabiNavi Pro AI", layout="centered")

# Initialize Session States for Bookmarks and Expenses
if "bookmarks" not in str_web.session_state:
    str_web.session_state.bookmarks = []
if "expenses" not in str_web.session_state:
    str_web.session_state.expenses = []

# --- 🌐 MULTI-LANGUAGE DICTIONARY ---
ui_translations = {
    "English": {
        "title": "🇯🇵 TabiNavi Pro AI",
        "sub": "Enterprise-Grade AI Travel Companion (Presentation Version)",
        "pref_label": "📍 Select Prefecture",
        "pref_holder": "Choose a prefecture...",
        "city_label": "🏙️ Select City / Area",
        "city_holder": "Choose a city...",
        "city_warn": "Please select a prefecture first.",
        "sec_quick": "🚀 Quick Travel Services",
        "train_btn": "🚄 Train & Routes",
        "food_btn": "🍣 Food & Dining",
        "hotel_btn": "🏨 Hotel Booking",
        "itinerary_btn": "🗺️ 3-Day Planner",
        "sec_ai_tools": "🧠 Advanced AI Travel Tools",
        "cam_box": "📸 Smart Camera Translator (Menu/Signboard)",
        "cam_upload": "Upload menu or signboard image...",
        "text_box": "🗣️ Real-time Speech/Text Translator",
        "text_input": "Enter text to translate...",
        "sec_pro": "🛡️ Pro Travel Tools & Utilities",
        "safety_box": "⚠️ Disaster Safety & Evacuation Guide",
        "safety_btn": "Get Emergency Guide",
        "expense_box": "💰 Travel Expense Tracker",
        "bookmark_box": "📌 Saved Locations & AI Summaries",
        "sec_trip": "🎯 Trip Activities & Etiquette",
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
        "sidebar_title": "⚙️ Project Control Panel",
    },
    "Myanmar": {
        "title": "🇯🇵 TabiNavi Pro AI",
        "sub": "အဆင့်မြင့် လုပ်ငန်းသုံး AI အိတ်ဆောင်ခရီးသွားလမ်းညွှန် (Presentation ဗားရှင်း)",
        "pref_label": "📍 ပြည်နယ်/ခရိုင် ကို ရွေးချယ်ပါ",
        "pref_holder": "ခရိုင်တစ်ခု ရွေးချယ်ပေးပါ...",
        "city_label": "🏙️ မြို့/ဒေသ ကို ရွေးချယ်ပါ",
        "city_holder": "မြို့ကို ရွေးချယ်ပေးပါ...",
        "city_warn": "အပေါ်တွင် ခရိုင်တစ်ခု အရင်ရွေးပေးပါ။",
        "sec_quick": "🚀 အမြန်အသုံးပြုနိုင်မည့် ဝန်ဆောင်မှုများ",
        "train_btn": "🚄 ရထားလမ်းကြောင်း",
        "food_btn": "🍣 အစားအသောက်ဆိုင်",
        "hotel_btn": "🏨 ဟိုတယ်တည်းခိုခန်း",
        "itinerary_btn": "🗺️ ၃ ရက်စာ ခရီးစဉ်",
        "sec_ai_tools": "🧠 အဆင့်မြင့် AI ခရီးသွားကိရိယာများ",
        "cam_box": "📸 Smart ကင်မရာ ဘာသာပြန်စနစ်",
        "cam_upload": "မီနူး သို့မဟုတ် ဆိုင်းဘုတ်ပုံရိပ် တင်ပေးပါ...",
        "text_box": "🗣️ အချိန်နဲ့တပြေးညီ စကားပြော/စာသား ဘာသာပြန်",
        "text_input": "ဘာသာပြန်လိုသည့် စာသားရိုက်ပါ...",
        "sec_pro": "🛡️ အဆင့်မြင့် ခရီးသွား အသုံးဆောင်များနှင့် စာရင်းများ",
        "safety_box": "⚠️ သဘာဝဘေးအန္တရာယ် ဘေးကင်းလုံခြုံရေး လမ်းညွှန်",
        "safety_btn": "အရေးပေါ် လမ်းညွှန်ချက်ရယူမည်",
        "expense_box": "💰 ခရီးသွားစရိတ် မှတ်တမ်းနှင့် စာရင်းချုပ်",
        "bookmark_box": "📌 မှတ်သားထားသော နေရာများနှင့် AI အချက်အလက်များ",
        "sec_trip": "🎯 ပြုလုပ်မည့် အတွေ့အကြုံများနှင့် စည်းကမ်းများ",
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
        "sidebar_title": "⚙️ ပရောဂျက် ထိန်းချုပ်ရေးခန်း",
    },
}

# --- ⚙️ SIDEBAR SETTINGS ---
with str_web.sidebar:
    str_web.markdown(f"## {ui_translations['English']['sidebar_title']}")
    language_options = {"🇺🇸 English": "English", "🇲🇲 Myanmar (မြန်မာ)": "Myanmar"}
    selected_lang_label = str_web.selectbox(
        "🌐 Interface Language", list(language_options.keys()), index=0
    )
    current_lang = language_options[selected_lang_label]
    tx = ui_translations[current_lang]
    str_web.markdown("---")
    str_web.info(
        "💡 Presentation Note: All responses use live streaming AI for mobile-app behavior simulation."
    )

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

# Location Dropdowns
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

common_ai_config = types.GenerateContentConfig(
    temperature=0.7,
    system_instruction=f"You are a local Japan travel expert. Respond using beautiful markdown with short, concise bullets. Output language: {current_lang}.",
)

# ----------------------------------------------------------------------
# 🚀 SECTION 1: QUICK TRAVEL SERVICES
# ----------------------------------------------------------------------
str_web.markdown("---")
str_web.subheader(tx["sec_quick"])

col1, col2, col3, col4 = str_web.columns(4)

if prefecture and city:
    loc_context = f"{city}, {prefecture}"
else:
    loc_context = "Tokyo"

with col1:
    if str_web.button(tx["train_btn"], use_container_width=True):
        if not prefecture:
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("🧠 Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Provide train/subway navigation guide for {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.info(full_text)

with col2:
    if str_web.button(tx["food_btn"], use_container_width=True):
        if not prefecture:
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("🧠 Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"List 3 must-try local restaurants/dishes in {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.success(full_text)

with col3:
    if str_web.button(tx["hotel_btn"], use_container_width=True):
        if not prefecture:
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("🧠 Connecting AI..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Recommend ideal tourist areas to book hotels in {loc_context}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.warning(full_text)

with col4:
    if str_web.button(tx["itinerary_btn"], use_container_width=True):
        if not prefecture:
            str_web.error(tx["error_select"])
        else:
            with str_web.spinner("🧠 Planning Itinerary..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Create a 3-day tourist itinerary for {loc_context} with Morning, Afternoon, Evening suggestions.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

# Bookmark Location Feature
if prefecture and city:
    if str_web.button(f"📌 Save {city} to My Bookmarks", use_container_width=True):
        bookmark_item = f"{city} ({prefecture})"
        if bookmark_item not in str_web.session_state.bookmarks:
            str_web.session_state.bookmarks.append(bookmark_item)
            str_web.toast(f"Saved {city} to your bookmarks panel!")

# --- MAPS ---
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

# ----------------------------------------------------------------------
# 🧠 SECTION 2: ADVANCED AI TOOLS
# ----------------------------------------------------------------------
str_web.markdown("---")
str_web.subheader(tx["sec_ai_tools"])

with str_web.expander(tx["cam_box"]):
    uploaded_file = str_web.file_uploader(tx["cam_upload"], type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        str_web.image(image, caption="Uploaded Image", width=250)
        if str_web.button("🔍 Translate Image Now", use_container_width=True):
            with str_web.spinner("🧠 Translating image text..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=[
                        f"Transcribe and translate into {current_lang} and explain:",
                        image,
                    ],
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

with str_web.expander(tx["text_box"]):
    input_text = str_web.text_input(tx["text_input"], placeholder="Type something...")
    if str_web.button("🌐 Translate Text", use_container_width=True):
        if input_text:
            with str_web.spinner("🧠 Translating..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Translate into Japanese, show Romaji and meaning for: '{input_text}'",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)

# ----------------------------------------------------------------------
# 🛡️ SECTION 3: PRO TRAVEL UTILITIES (Bookmarks, Disaster & Expense)
# ----------------------------------------------------------------------
str_web.markdown("---")
str_web.subheader(tx["sec_pro"])

# Disaster Safety Guide
with str_web.expander(tx["safety_box"]):
    str_web.write(
        "Get instant emergency guides for earthquakes, tsunamis, or typhoons."
    )
    if str_web.button(tx["safety_btn"], use_container_width=True):
        with str_web.spinner("🚨 Generating Safe Evacuation Steps..."):
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=f"Provide critical evacuation steps, safety apps, and survival tips for foreign tourists during an earthquake or disaster in {loc_context}.",
                config=common_ai_config,
            ):
                full_text += chunk.text
                placeholder.error(full_text)

# Travel Expense Tracker
with str_web.expander(tx["expense_box"]):
    col_item, col_cost = str_web.columns([2, 1])
    with col_item:
        exp_name = str_web.text_input(
            "Expense Item", placeholder="e.g., Ramen dinner, Shinkansen Ticket"
        )
    with col_cost:
        exp_amt = str_web.number_input("Amount (JPY)", min_value=0, step=100)
    if str_web.button("➕ Add Expense", use_container_width=True):
        if exp_name and exp_amt > 0:
            str_web.session_state.expenses.append({"item": exp_name, "cost": exp_amt})
            str_web.toast("Expense added successfully!")

    if str_web.session_state.expenses:
        total_spent = sum(item["cost"] for item in str_web.session_state.expenses)
        str_web.markdown(f"### Total Spent: **{total_spent:,} JPY**")
        for i, item in enumerate(str_web.session_state.expenses):
            str_web.text(f"• {item['item']}: {item['cost']:,} JPY")
        if str_web.button("🗑️ Clear All Expenses"):
            str_state = str_web.session_state
            str_state.expenses = []
            str_web.rerun()

# Bookmarks Display
with str_web.expander(tx["bookmark_box"]):
    if str_web.session_state.bookmarks:
        for mark in str_web.session_state.bookmarks:
            str_web.markdown(f"📌 **{mark}**")
        if str_web.button("🗑️ Clear Bookmarks"):
            str_state = str_web.session_state
            str_state.bookmarks = []
            str_web.rerun()
    else:
        str_web.write("No locations bookmarked yet.")

# ----------------------------------------------------------------------
# --- SECTION 4: TRIP ACTIVITIES & ETIQUETTE ---
# ----------------------------------------------------------------------
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
)

with str_web.expander(tx["guide_box"]):
    if str_web.button(tx["guide_btn"], key="exp_guide"):
        if prefecture and city and experience_type:
            with str_web.spinner("Loading..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Provide etiquette guide for '{experience_type}' in {city}, {prefecture}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)
        else:
            str_web.error("⚠️ Please select choices first!")

with str_web.expander(tx["weather_box"]):
    if str_web.button(tx["weather_btn"], key="exp_weather"):
        if prefecture and city:
            with str_web.spinner("Loading..."):
                placeholder = str_web.empty()
                full_text = ""
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=f"Provide weather and clothing guide for {city}, {prefecture}.",
                    config=common_ai_config,
                ):
                    full_text += chunk.text
                    placeholder.markdown(full_text)
        else:
            str_web.error(tx["error_select"])

with str_web.expander(tx["calc_box"]):
    currency_target = str_web.selectbox(
        "Target Currency", ["MMK (Myanmar Kyat)", "USD (US Dollar)"]
    )
    yen_amount = str_web.number_input(
        "Amount in JPY", min_value=0, value=1000, step=500
    )
    if str_web.button(tx["calc_btn"], key="exp_calc"):
        with str_web.spinner("Calculating..."):
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=f"Convert {yen_amount} JPY to {currency_target} with realistic current rates.",
                config=common_ai_config,
            ):
                full_text += chunk.text
                placeholder.markdown(full_text)

with str_web.expander(tx["sos_box"]):
    if str_web.button(tx["sos_btn"], key="exp_sos"):
        with str_web.spinner("Loading..."):
            placeholder = str_web.empty()
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=f"Provide emergency numbers in Japan and 1 foreign-friendly hospital near {city if city else 'Tokyo'}.",
                config=common_ai_config,
            ):
                full_text += chunk.text
                placeholder.markdown(full_text)
