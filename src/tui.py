from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Vertical
from textual.widgets import Header, Footer, DataTable, Static, Input, Button
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import ListView, ListItem, Label
from scanner import scan_network
from database import is_registered, add_device, remove_device, get_device_name
import sys

class NameInputScreen(Screen):
    """Écran pour saisir le nom d'un appareil"""

    def __init__(self, device_data):
        super().__init__()
        self.device_data = device_data

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Enter device name:", id="prompt")
            yield Input(placeholder="Device name", id="name_input")
            yield Button("Save", id="save_button")
            yield Button("Cancel", id="cancel_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_button":
            name_input = self.query_one("#name_input", Input)
            ip, mac, vendor = self.device_data
            name = name_input.value.strip()
            if name:
                add_device(ip, mac, vendor, name)
            else:
                add_device(ip, mac, vendor)
        self.app.pop_screen()
        self.app.refresh_table()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()

class DeviceDetails(Static):
    """Widget pour afficher les détails d'un appareil"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.styles.background_color = "blue"
        self.styles.padding = (1, 2)

    def update_details(self, device_data):
        if device_data:
            ip, mac, vendor = device_data
            name = get_device_name(mac) or "Not set"
            self.update(f"""Device Name: {name}\nIP Address: {ip}\nMAC Address: {mac}\nVendor: {vendor}\nStatus: {"Registered" if is_registered(mac) else "Unregistered"}""")
        else:
            self.update("No device selected")

class SortScreen(Screen):
    """Écran pour sélectionner la colonne de tri"""
    
    def compose(self) -> ComposeResult:
        items = [
            ListItem(Label("IP Address")),
            ListItem(Label("MAC Address")),
            ListItem(Label("Vendor"))
        ]
        yield ListView(*items)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        column = event.item.children[0].render()
        self.app.sort_by_column(column)
        self.app.pop_screen()

class NetworkScannerApp(App):
    BINDINGS = [
        Binding("ctrl+r", "refresh", "Refresh Scan"),
        Binding("ctrl+s", "show_sort", "Sort Data"),
        Binding("up", "move_up", "Move Up"),
        Binding("down", "move_down", "Move Down"),
        Binding("enter", "toggle_device", "Toggle Registration"),
        *App.BINDINGS
    ]

    def __init__(self, interface='eth0'):
        super().__init__()
        self.interface = interface
        self.current_devices = []
        self.selected_row = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(DataTable(id="device_table"))
        yield DeviceDetails(id="device_details")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_table()

    def refresh_table(self):
        try:
            table = self.query_one("#device_table", DataTable)
            table.clear()
            if not table.columns:
                table.add_columns("Status", "IP Address", "MAC Address", "Vendor")
            else:
                table.clear()
            self.current_devices = scan_network(self.interface)
            for ip, mac, vendor in self.current_devices:
                status = "✅" if is_registered(mac) else "❌"
                table.add_row(status, ip, mac, vendor)
            self.selected_row = 0
            self.update_details()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            self.exit()

    def update_details(self):
        details = self.query_one("#device_details", DeviceDetails)
        if 0 <= self.selected_row < len(self.current_devices):
            details.update_details(self.current_devices[self.selected_row])
        else:
            details.update_details(None)

    def action_move_up(self) -> None:
        """Déplacer la sélection vers le haut"""
        if self.current_devices:
            table = self.query_one("#device_table", DataTable)
            self.selected_row = max(0, self.selected_row - 1)
            table.cursor_coordinate = (self.selected_row, 0)
            self.update_details()

    def action_move_down(self) -> None:
        """Déplacer la sélection vers le bas"""
        if self.current_devices:
            table = self.query_one("#device_table", DataTable)
            self.selected_row = min(len(self.current_devices) - 1, self.selected_row + 1)
            table.cursor_coordinate = (self.selected_row, 0)
            self.update_details()

    def update_table_with_sorted_data(self, sorted_devices):
        try:
            table = self.query_one("#device_table", DataTable)
            table.clear()
            for ip, mac, vendor in sorted_devices:
                status = "✅" if is_registered(mac) else "❌"
                table.add_row(status, ip, mac, vendor)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

    def action_refresh(self) -> None:
        """Rafraîchir le scan"""
        self.refresh_table()

    def action_show_sort(self) -> None:
        """Afficher l'écran de sélection de tri"""
        self.push_screen(SortScreen())

    def sort_by_column(self, column: str) -> None:
        """Trier les données selon la colonne sélectionnée"""
        if not self.current_devices:
            return

        index = {"IP Address": 0, "MAC Address": 1, "Vendor": 2}
        if column in index:
            sorted_devices = sorted(self.current_devices, key=lambda x: x[index[column]])
            self.update_table_with_sorted_data(sorted_devices)

    def action_toggle_device(self) -> None:
        """Basculer l'enregistrement d'un appareil"""
        if not self.current_devices or self.selected_row >= len(self.current_devices):
            return
    
        device = self.current_devices[self.selected_row]
        ip, mac, vendor = device
    
        if is_registered(mac):
            remove_device(mac)
            self.refresh_table()
        else:
            # Afficher l'écran de saisie du nom
            self.push_screen(NameInputScreen(device))