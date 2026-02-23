import flet as ft

def run_weather_monitor(page: ft.Page):
    page.title = "Метео Сводка"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 480
    page.window_height = 750
    
    locations = (
        "Чуй", "Ош", "Баткен", "Нарын", 
        "Иссык-Куль", "Талас", "Джалал-Абад"
    )
    
    inputs_map = {}
    output_area = ft.Column(spacing=5)

    def process_stats(e):
        try:
            raw_data = {loc: float(inputs_map[loc].value) for loc in locations}
            
            all_temps = list(raw_data.values())
            avg = sum(all_temps) / len(all_temps)
            
            warmest = max(raw_data, key=raw_data.get)
            coldest = min(raw_data, key=raw_data.get)

            status_color = ft.Colors.BLUE_800
            if avg > 20:
                status_color = ft.Colors.ORANGE_800
            elif avg < 10:
                status_color = ft.Colors.LIGHT_BLUE_400

            output_area.controls = [
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.THERMOSTAT, color=status_color),
                    title=ft.Text(f"Средний показатель: {avg:.1f}°C", color=status_color, weight="bold"),
                    subtitle=ft.Text(f"Пик: {raw_data[warmest]}° ({warmest})\nМинимум: {raw_data[coldest]}° ({coldest})"),
                )
            ]
        except:
            output_area.controls = [ft.Text("Ошибка ввода данных", color=ft.Colors.RED_700)]
        
        page.update()

    fields_container = ft.Column(spacing=10)
    
    for loc in locations:
        tf = ft.TextField(
            label=loc,
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            suffix_icon=ft.Icons.LOCATION_ON_OUTLINED,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        inputs_map[loc] = tf
        fields_container.controls.append(tf)

    main_view = ft.ListView(
        expand=True,
        spacing=20,
        padding=20,
        controls=[
            ft.Text("Температурный режим КР", size=26, weight="bold"),
            fields_container,
            ft.FilledButton(
                "Сформировать отчет",
                icon=ft.Icons.QUERY_STATS,
                on_click=process_stats,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            ),
            ft.Container(
                content=output_area,
                padding=10,
                bgcolor=ft.Colors.GREY_100,
                border_radius=10
            )
        ]
    )

    page.add(main_view)

if __name__ == "__main__":
    ft.app(target=run_weather_monitor)