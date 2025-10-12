import flet as ft

locations = [
    {"name": "Main Library", "category": "Library", "description": "Largest library", "x": 100, "y": 150},
    {"name": "Engineering Building", "category": "Academic", "description": "Engineering labs", "x": 300, "y": 250},
    {"name": "Student Union", "category": "Social", "description": "Relax and eat", "x": 500, "y": 100},
    {"name": "Health Center", "category": "Service", "description": "Medical services", "x": 200, "y": 400},
    {"name": "Campus Cafe", "category": "Social", "description": "Coffee spot", "x": 450, "y": 350},
    {"name": "Physics Department", "category": "Academic", "description": "Physics department", "x": 350, "y": 50},
]

def main(page: ft.Page):
    page.title = "Campus Map with Animated Panel"
    page.window_width = 400   # width in pixels
    page.window_height = 700  # height in pixels
    page.padding = 0

    offset_x = 0
    offset_y = 0
    scale = 1.0

    def darkmode(e):
        if darkmodee.value==False:
            page.theme_mode="light"
            search_bar.color="green"
            right_panel.bgcolor="white"

            page.update()
        elif darkmodee.value==True:
            page.theme_mode="dark"
            right_panel.bgcolor="grey"
            search_bar.color="grey"
            page.update()

    # --- Right-side panel ---
    panel_width = 200
    panel_visible = False
    darkmodee=ft.CupertinoSwitch(
                   
                    label="",
                    focus_color="red",
                    value=False,
                    on_change=darkmode)
    
    right_panel = ft.Container(
        content=ft.Column(
            [
                ft.Text("Panel", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                darkmodee
               
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=panel_width,
        height=page.window_height,
        bgcolor="white",
        padding=15,
        right=-panel_width,  # Start hidden outside screen
        top=0,
        animate_position=300,  # Animation duration in ms
    )

    # --- Search bar ---
    search_bar = ft.TextField(
        hint_text="Search location...",
        prefix_icon="search",
        
        border_radius=25,
        bgcolor="white",
        color="black",
        border_color="grey",
    )

    # --- Toggle button (top-right) ---
    toggle_button = ft.FloatingActionButton(
        icon="menu",
        right=20,
        top=20,
    )

    def toggle_panel(e):
        nonlocal panel_visible
        panel_visible = not panel_visible
        right_panel.right = 0 if panel_visible else -panel_width
        page.update()

    toggle_button.on_click = toggle_panel

    # --- Map background ---
    map_img = ft.Image(
        src="/campus_map.png",
        
    )

    # --- Markers ---
    location_markers = []
    for loc in locations:
        marker = ft.Container(
            content=ft.Icon("location_on", color="red", size=30),
            left=loc["x"],
            top=loc["y"],
            data=loc,
        )
        location_markers.append(marker)

    # --- Map stack ---
    map_stack = ft.Stack([map_img, *location_markers])

    # --- Update positions for pan & zoom ---
    def update_map():
        map_img.width = 1000 * scale
        map_img.height = 800 * scale
        map_img.left = offset_x
        map_img.top = offset_y
        for m in location_markers:
            loc = m.data
            m.left = offset_x + loc["x"] * scale
            m.top = offset_y + loc["y"] * scale
        page.update()

    # --- Drag (pan) ---
    def on_pan(e: ft.DragUpdateEvent):
        nonlocal offset_x, offset_y
        offset_x += e.delta_x
        offset_y += e.delta_y
        update_map()

    gesture_layer = ft.GestureDetector(
        content=map_stack,
        on_pan_update=on_pan,
    )

    # --- Zoom Slider ---
    zoom_slider = ft.Slider(min=0.5, max=3, value=1, divisions=25, label="{value}x")
    def on_zoom(e):
        nonlocal scale
        scale = e.control.value
        update_map()
    zoom_slider.on_change = on_zoom

    #buttons___

    bttn1=ft.FilledButton(
        text="SWITCH TO 3D MODE"
    )

    # --- Layout ---
    page.add(
        ft.Stack([
            gesture_layer,                                           # Map layer
            ft.Container(content=search_bar, top=20, left=20, width=300),  # Search bar top-left
            right_panel,                                             # Right-side animated panel
            ft.Container(content=zoom_slider, bottom=20, left=20, width=200),  # Zoom slider
            toggle_button,
            ft.Container(content=bttn1, bottom=100, left=90, width=200),  # Zoom slider
            toggle_button
            
                                                       
                                                                                                  # Toggle button top-most
        ], expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main, 
           assets_dir="assets")
