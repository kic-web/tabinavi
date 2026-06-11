import os
import json
import flet as ft
from google import genai
from google.genai import types

def main(page: ft.Page):
    # 🌟 1. Page Configuration (Premium PC App)
    page.title = "TabiNavi Concierge"
    page.theme_mode = ft.ThemeMode.DARK
    page.background_color = "#0E1117"  # Streamlit မူရင်း Dark Theme နောက်ခံ
    page.padding = 0  
    page.window_width = 1240
    page.window_height = 900

    # 🔑 Gemini API Key
    API_KEY = "AIzaSy..." 
    client = genai.Client(api_key=API_KEY)

    # 📂 Japan Data Load လုပ်ခြင်း
    json_path = os.path.join(os.path.dirname(__file__), "..", "japan_data.json")
    prefecture_city_map = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            prefecture_city_map = json.load(f)

    # --- 🛠️ 2. Core Logic (လုပ်ဆောင်ချက်များ) ---
    def on_pref_change(e):
        selected_pref = pref_dropdown.value
        if selected_pref in prefecture_city_map:
            # ✅ Flet ဗားရှင်းသစ်နဲ့ ကွက်တိကိုက်ညီအောင် ပြင်ဆင်ထားသော Option List
            city_dropdown.options = [ft.dropdown.Option(text=str(c), key=str(c)) for c in prefecture_city_map[selected_pref]]
            city_dropdown.disabled = False
        else:
            city_dropdown.disabled = True
            city_dropdown.options = []
        city_dropdown.value = None
        page.update()

    def handle_service_call(prompt_text):
        output_box.value = "⏳ AI က ရှာဖွေပေးနေပါသည်..."
        page.update()
        try:
            config = types.GenerateContentConfig(
                temperature=0.7,
                system_instruction=f"Provide helpful Japan travel insights in Myanmar language. User preferred language is {lang_dropdown.value}."
            )
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_text, config=config)
            output_box.value = response.text
        except Exception as ex:
            output_box.value = f"⚠️ Connection Error: {str(ex)}"
        page.update()

    # Tools & Language Actions
    def on_lang_change(e):
        output_box.value = f"🌐 Language switched to: {lang_dropdown.value}"
        page.update()

    def click_camera_tool(e):
        output_box.value = f"📷 [Smart Camera Translator Activated] Ready to scan Japanese text into {lang_dropdown.value}..."
        page.update()

    def click_speech_tool(e):
        output_box.value = f"🗣️ [Text/Speech Translator Activated] Listening for speech inputs..."
        page.update()

    # Custom Trip Planner Logic
    def generate_custom_plan(e):
        if not city_dropdown.value:
            output_box.value = "💡 Please select a Destination (Prefecture & City) first!"
            page.update()
            return
        if not days_dropdown.value:
            output_box.value = "📅 Please select the number of days for your trip!"
            page.update()
            return
        
        prompt = f"Create a detailed travel itinerary for {days_dropdown.value} in {city_dropdown.value}. Suggest top places and scheduling."
        handle_service_call(prompt)

    # Login Logic
    def handle_login(e):
        if username_input.value and password_input.value:
            login_status.value = f"✅ Welcome back, {username_input.value}! (Premium Active)"
            login_status.color = ft.Colors.GREEN_400
        else:
            login_status.value = "⚠️ Please enter both Username and Password."
            login_status.color = ft.Colors.RED_400
        page.update()

    def check_weather(e):
        if city_dropdown.value:
            weather_text.value = f"☀️ 15°C\nCloudy in {city_dropdown.value}"
        else:
            weather_text.value = "💡 Please select a city first."
        page.update()

    def calculate_currency(e):
        try:
            amount = float(currency_input.value) if currency_input.value else 1000
            usd_rate = amount / 154  
            currency_result.value = f"💵 Result: {amount} JPY = ${usd_rate:.2f} USD"
        except:
            currency_result.value = "⚠️ Invalid Amount"
        page.update()

    # --- 🛠️ 3. LEFT SIDEBAR (Control Panel & Tools) ---
    # ✅ Dropdown ရဲ့ စံနှုန်းအမှန်အတိုင်း သေချာပြန်ပြင်ထားပါတယ်
    lang_dropdown = ft.Dropdown(
        value="English",
        options=[
            ft.dropdown.Option(text="English", key="English"), 
            ft.dropdown.Option(text="Myanmar", key="Myanmar"),
            ft.dropdown.Option(text="Japanese (JP)", key="Japanese (JP)")
        ],
        border_color="#3A4454",
        bgcolor="#1A202C",
        on_change=on_lang_change  
    )

    sidebar_content = ft.Container(
        content=ft.Column([
            ft.Text("⚙️ Control Panel", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Divider(color="#2D3748"),
            
            ft.Text("🌐 Language", size=14, color="#B0C4DE"),
            lang_dropdown,
            
            ft.Divider(color="#2D3748"),
            ft.Text("🛠️ Translation Tools", size=14, color="#B0C4DE"),
            ft.ElevatedButton("📷 Smart Camera Translator", width=260, on_click=click_camera_tool, style=ft.ButtonStyle(bgcolor="#1F2937")),
            ft.ElevatedButton("🗣️ Text/Speech Translator", width=260, on_click=click_speech_tool, style=ft.ButtonStyle(bgcolor="#1F2937")),
        ], spacing=15),
        bgcolor="#1F2937",
        padding=20,
        width=300,
        height=900
    )

    # --- 🛠️ 4. LOGIN PANEL ---
    username_input = ft.TextField(label="Username", width=160, height=40, text_size=13, border_color="#3A4454")
    password_input = ft.TextField(label="Password", password=True, can_reveal_password=True, width=160, height=40, text_size=13, border_color="#3A4454")
    login_status = ft.Text("Please login to sync travel data.", size=12, color="#718096")
    
    login_bar = ft.Container(
        content=ft.Row([
            ft.Text("🔐 Member Login:", size=14, weight=ft.FontWeight.BOLD),
            username_input,
            password_input,
            ft.ElevatedButton("Sign In", on_click=handle_login, style=ft.ButtonStyle(bgcolor="#2D3748")),
            login_status
        ], spacing=15, alignment=ft.MainAxisAlignment.START),
        padding=10,
        bgcolor="#141B26",
        border_radius=8,
        width=850
    )

    # --- 🛠️ 5. RIGHT MAIN CONTENT PANEL ---
    header_card = ft.Container(
        content=ft.Column([
            ft.Text("TabiNavi Concierge", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text("Your Next-Gen AI Travel Companion", size=14, color="#B0C4DE")
        ], alignment=ft.MainAxisAlignment.CENTER),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
            colors=["#1D5B66", "#0F3A40"]
        ),
        padding=25, border_radius=12, width=850
    )

    # Destination Dropdowns
    pref_dropdown = ft.Dropdown(
        label="Select Prefecture", 
        options=[ft.dropdown.Option(text=str(p), key=str(p)) for p in prefecture_city_map.keys()], 
        on_change=on_pref_change, 
        border_color="#3A4454", 
        expand=True
    )
    city_dropdown = ft.Dropdown(label="Select City / Area", disabled=True, border_color="#3A4454", expand=True)
    destination_row = ft.Row([pref_dropdown, city_dropdown], spacing=15, width=850)

    # Trip Planner Section (ရက်အလိုက် ရွေးချယ်နိုင်သော စနစ်သစ်)
    days_dropdown = ft.Dropdown(
        label="Select Number of Days",
        options=[ft.dropdown.Option(text=f"{i} Days Plan", key=f"{i} Days") for i in range(1, 11)], 
        border_color="#3A4454",
        expand=True
    )
    make_plan_btn = ft.ElevatedButton("📅 Generate Custom Plan", on_click=generate_custom_plan, style=ft.ButtonStyle(bgcolor="#1D5B66", color=ft.Colors.WHITE), height=50)
    plan_section_row = ft.Row([days_dropdown, make_plan_btn], spacing=15, width=850)

    # Core Travel Service Buttons
    btn_route = ft.ElevatedButton("🚄 Routes Guide", on_click=lambda e: handle_service_call(f"Provide train routes to {city_dropdown.value}"), style=ft.ButtonStyle(bgcolor="#1F2937", color=ft.Colors.WHITE), expand=True, height=50)
    btn_food = ft.ElevatedButton("🍱 Food & Dining", on_click=lambda e: handle_service_call(f"List famous food in {city_dropdown.value}"), style=ft.ButtonStyle(bgcolor="#1F2937", color=ft.Colors.WHITE), expand=True, height=50)
    btn_hotel = ft.ElevatedButton("🏨 Hotels", on_click=lambda e: handle_service_call(f"Best hotel areas in {city_dropdown.value}"), style=ft.ButtonStyle(bgcolor="#1F2937", color=ft.Colors.WHITE), expand=True, height=50)
    services_row = ft.Row([btn_route, btn_food, btn_hotel], spacing=15, width=850)
    
    bookmark_btn = ft.ElevatedButton("⭐ Save City to Bookmarks", width=850, style=ft.ButtonStyle(bgcolor="#2D3748"))

    # Map Card
    map_container = ft.Container(
        content=ft.Row([
            ft.Text("🗺️ [Map View Integrated Placeholder]", color="#718096", size=14, expand=True),
            ft.ElevatedButton("Open in Maps ↗", url="https://maps.google.com")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor="#1F2937", padding=15, border_radius=10, width=850
    )

    # Weather & Currency Layout
    weather_text = ft.Text("⛅ 15°C\nWeather Info", size=12, weight=ft.FontWeight.BOLD)
    currency_result = ft.Text("🇺🇸 1$ = 154¥ 🇯🇵", size=12, weight=ft.FontWeight.BOLD)
    weather_card = ft.Container(content=weather_text, bgcolor="#1F2937", padding=15, border_radius=10, expand=True)
    currency_card = ft.Container(content=currency_result, bgcolor="#1F2937", padding=15, border_radius=10, expand=True)
    
    currency_input = ft.TextField(label="Amount in JPY", value="1000", border_color="#3A4454", height=45, expand=True)
    calc_btn = ft.ElevatedButton("Calculate", on_click=calculate_currency, height=45)

    # Utilities Panel
    utilities_content = ft.Container(
        content=ft.Column([
            ft.Text("🚨 [Disaster Safety Guide]", weight=ft.FontWeight.BOLD, size=14),
            ft.Text("• Earthquake: Drop, Cover, Hold on.\n• Tsunami: Move to higher ground immediately.", size=13),
            ft.Divider(color="#2D3748"),
            ft.Text("📊 Travel Expense Tracker: Feature Ready", size=13, color="#B0C4DE"),
            ft.Text("⭐ Saved Locals: Saved Locations List", size=13, color="#B0C4DE"),
        ]),
        bgcolor="#141B26", padding=15, border_radius=10, width=850
    )

    # Output Box View
    output_box = ft.Text("ခရီးသွားလမ်းညွှန်ချက်များနှင့် အချက်အလက်များကို ဤနေရာတွင် ပြသပေးမည်။", size=13)
    output_container = ft.Container(
        content=ft.Column([output_box], scroll=ft.ScrollMode.AUTO),
        bgcolor="#1A202C", padding=15, border_radius=10,
        border=ft.Border.all(1, "#2D3748"), width=850, height=200 
    )

    # Right Side Content Assembly
    main_content_area = ft.Container(
        content=ft.Column([
            login_bar, 
            header_card,
            ft.Text("Select Destination", size=16, weight=ft.FontWeight.BOLD),
            destination_row,
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
            ft.Text("Trip Planner (Select Days)", size=16, weight=ft.FontWeight.BOLD),
            plan_section_row, 
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
            ft.Text("Quick Travel Services", size=16, weight=ft.FontWeight.BOLD),
            services_row,
            bookmark_btn,
            ft.Divider(height=10),
            map_container,
            ft.Divider(height=10),
            ft.Text("Trip Activities & Local Etiquette", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([weather_card, currency_card], spacing=15, width=850),
            ft.ElevatedButton("Check Weather", on_click=check_weather, width=850),
            ft.Row([currency_input, calc_btn], spacing=15, width=850),
            ft.Divider(height=10),
            ft.Text("Travel Utilities", size=16, weight=ft.FontWeight.BOLD),
            utilities_content,
            output_container
        ], spacing=15, scroll=ft.ScrollMode.AUTO),
        padding=25,
        expand=True
    )

    # --- 🌟 6. MAIN LAYOUT SPLIT ---
    page.add(
        ft.Row([
            sidebar_content,
            main_content_area
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    ft.run(main)