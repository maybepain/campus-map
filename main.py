import flet as ft

locations = [
    {"name": "Main Library", "category": "Library", "description": "Largest library", "x": 100, "y": 150},
    {"name": "Engineering Building", "category": "Academic", "description": "Engineering labs", "x": 300, "y": 250},
    {"name": "Student Union", "category": "Social", "description": "Relax and eat", "x": 500, "y": 100},
    {"name": "Health Center", "category": "Service", "description": "Medical services", "x": 200, "y": 400},
    {"name": "Campus Cafe", "category": "Social", "description": "Coffee spot", "x": 450, "y": 350},
    {"name": "Physics Department", "category": "Academic", "description": "Physics department", "x": 350, "y": 50},
]

MAP_BASE_WIDTH = 1000
MAP_BASE_HEIGHT = 800

def main(page: ft.Page):
    page.title = "Campus Map with Animated Panel"
    
    
    page.padding = 0
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = True
    page.bgcolor = "black"

    offset_x = 0
    offset_y = 0
    scale = 1.0

    # ---- Dark mode toggle ----
    def darkmode(e):
        if not darkmodee.value:
            page.theme_mode = "light"
            search_bar.color = "green"
            right_panel.bgcolor = "white"
        else:
            page.theme_mode = "dark"
            right_panel.bgcolor = "black"
            search_bar.color = "black"
        page.update()

    darkmodee=ft.CupertinoSwitch(
                label="",
                focus_color="red",
                value=False,
                on_change=darkmode
            )


    #darkmode
    darkmodeall=ft.Row(
        controls=[
            ft.Text(value="light"),
            darkmodee,
            ft.Text(value="dark")

        ]
    )

    #satelite mode
    def satelite(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            mapimg.src="assets/campus_map2.png"
            
        elif selected_index == 1:
            mapimg.src="assets/campusap.png"
            
        elif selected_index == 2:
            pass
           
        

            page.update()
            
        
        page.update()

        
    #downpanel items
    satelitebutt=ft.NavigationBarDestination(icon=ft.Icons.SATELLITE_ALT,label="NORMAL MODE")
    satelitebutt2=ft.NavigationBarDestination(icon=ft.Icons.SATELLITE_ALT,label="SATALITE MODE")


    #downpanel
    downbar=ft.NavigationBar(
        destinations=[
            satelitebutt,
            satelitebutt2,
            ft.NavigationBarDestination(icon=ft.Icons.THREED_ROTATION,label="3D MODE"),
            ft.NavigationBarDestination(icon=ft.Icons.CAMERA_ALT,label="CAMARA MODE"),
            
           


        ],on_change=satelite
    )

    # --- Right-side panel ---
    panel_width = 200
    panel_visible = False
   
   

    right_panel = ft.Container(
        content=ft.Column(
            [
                ft.Text("Panel", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                darkmodeall
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=panel_width,
        height=page.height,
        bgcolor="#b2b2b2",
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
    toggle_button = ft.FloatingActionButton(icon="menu", right=20, top=20, )

    def toggle_panel(e):
        nonlocal panel_visible
        panel_visible = not panel_visible
        right_panel.right = 0 if panel_visible else -panel_width
        page.update()

    toggle_button.on_click = toggle_panel

    #img backround
    mapimg=ft.Image(
            src="assets/campus_map2.png",
            fit=ft.ImageFit.COVER,
            width=MAP_BASE_WIDTH,
            height=MAP_BASE_HEIGHT
        )

    # --- Map background ---
    map_container = ft.Container(
        content=mapimg,
        left=0,
        top=0,
        expand=True,
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
    map_stack = ft.Stack([map_container, *location_markers], expand=True)

    # --- Update positions for pan & zoom ---
    def update_map():
        nonlocal offset_x, offset_y
        map_width = MAP_BASE_WIDTH * scale
        map_height = MAP_BASE_HEIGHT * scale

        # Clamp offsets
        max_offset_x = 0
        min_offset_x = page.width - map_width
        max_offset_y = 0
        min_offset_y = page.height - map_height
        offset_x_clamped = min(max_offset_x, max(min_offset_x, offset_x))
        offset_y_clamped = min(max_offset_y, max(min_offset_y, offset_y))
        offset_x = offset_x_clamped
        offset_y = offset_y_clamped

        map_container.width = map_width
        map_container.height = map_height
        map_container.left = offset_x
        map_container.top = offset_y

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
        expand=True,
    )

    # --- Zoom Slider ---
    zoom_slider = ft.Slider(min=0.5, max=3, value=1, divisions=25, label="{value}x")

    def on_zoom(e):
        nonlocal scale
        scale = e.control.value
        update_map()

    zoom_slider.on_change = on_zoom

    # --- 3D Button ---
    bttn1 = ft.FilledButton(text="SWITCH TO 3D MODE")
    #bttn2 = ft.FilledButton(text="SWITCH TO CAMARA MODE")
    

    # --- Handle window resize ---
    def on_resize(e):
        update_map()

    page.on_resize = on_resize

    # --- Layout ---
    page.add(
        ft.Stack([
            gesture_layer,
            ft.Container(content=search_bar, top=20, left=20, width=300),
            right_panel,
            ft.Container(content=zoom_slider, bottom=20, left=20, width=200),
            ft.Container(content=downbar, bottom=0, left=0, width=400),
            toggle_button
        ], expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
