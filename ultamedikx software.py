import sqlite3
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window

screen_helper = """
MDNavigationLayout:
    MDScreenManager:
        id: screen_manager
        MDScreen:
            name: 'home'
            BoxLayout:
                orientation: 'vertical'
                padding: '10dp'
                spacing: '10dp'
                MDTopAppBar:
                    title: 'Ultramedikx Accounting Software'
                    elevation: 4
                    md_bg_color: app.theme_cls.primary_color
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                Image:
                    source: 'pexel.jpg'
                    allow_stretch: True
                    keep_ratio: False
                    size_hint_y: None
                    height: dp(520)
                Widget:
        MDScreen:
            name: 'add_entry'
            BoxLayout:
                orientation: 'vertical'
                padding: '10dp'
                spacing: '10dp'
                MDTopAppBar:
                    title: 'Add Entry'
                    elevation: 4
                    md_bg_color: app.theme_cls.primary_color
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        spacing: '10dp'
                        MDTextField:
                            id: date
                            hint_text: "Date (YYYY-MM-DD)"
                        MDTextField:
                            id: cash_in
                            hint_text: "Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: pos_cash_in
                            hint_text: "POS Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: transfers_cash_in
                            hint_text: "Transfers Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: retainership_cash_in
                            hint_text: "Retainership Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: outstanding_cash_in
                            hint_text: "Outstanding Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: expenditure_cash_out
                            hint_text: "Expenditure Cash Out"
                            input_filter: "float"
                        MDRaisedButton:
                            text: "Submit"
                            md_bg_color: app.theme_cls.primary_color
                            on_release: app.submit_entry()
        MDScreen:
            name: 'update_entry'
            BoxLayout:
                orientation: 'vertical'
                padding: '10dp'
                spacing: '10dp'
                MDTopAppBar:
                    title: 'Update Entry'
                    elevation: 4
                    md_bg_color: app.theme_cls.primary_color
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        spacing: '10dp'
                        MDTextField:
                            id: entry_id
                            hint_text: "Entry ID"
                            input_filter: "int"
                        MDTextField:
                            id: update_date
                            hint_text: "Date (YYYY-MM-DD)"
                        MDTextField:
                            id: update_cash_in
                            hint_text: "Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: update_transfers_cash_in
                            hint_text: "Transfers Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: update_retainership_cash_in
                            hint_text: "Retainership Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: update_outstanding_cash_in
                            hint_text: "Outstanding Cash In"
                            input_filter: "float"
                        MDTextField:
                            id: update_expenditure_cash_out
                            hint_text: "Expenditure Cash Out"
                            input_filter: "float"
                        MDRaisedButton:
                            text: "Update"
                            md_bg_color: app.theme_cls.primary_color
                            on_release: app.update_entry()
                            
        MDScreen:
            name: 'view_entries'
            BoxLayout:
                orientation: 'vertical'
                padding: '10dp'
                spacing: '10dp'
                MDTopAppBar:
                    title: 'View Entries'
                    elevation: 4
                    md_bg_color: app.theme_cls.primary_color
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                BoxLayout:
                    id: table_box
                    orientation: 'vertical'
                    padding: '10dp'
                    spacing: '10dp'
                MDRaisedButton:
                    text: "Clear All Entries"
                    md_bg_color: app.theme_cls.primary_color
                    on_release: app.show_clear_confirmation_dialog()
        MDScreen:
            name: 'monthly_summary'
            BoxLayout:
                orientation: 'vertical'
                padding: '10dp'
                spacing: '10dp'
                MDTopAppBar:
                    title: 'Monthly Summary'
                    elevation: 4
                    md_bg_color: app.theme_cls.primary_color
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        spacing: '10dp'
                        MDTextField:
                            id: summary_month
                            hint_text: "Enter Month (YYYY-MM)"
                        MDRaisedButton:
                            text: "Get Summary"
                            md_bg_color: app.theme_cls.primary_color
                            on_release: app.get_monthly_summary()
                        MDLabel:
                            id: summary_text
                            text: "Summary will appear here"
                            theme_text_color: "Secondary"

    MDNavigationDrawer:
        id: nav_drawer
        BoxLayout:
            orientation: 'vertical'
            spacing: '8dp'
            padding: '8dp'
            Image:
                source: 'images.png'
            MDLabel:
                text: " ULTRAMEDIKX"
                font_style: 'Subtitle1'
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                text: " Ultramedikx Pathology Laboratory"
                font_style: 'Caption'
                size_hint_y: None
                height: self.texture_size[1]
            ScrollView:
                MDList:
                    OneLineIconListItem:
                        text: 'Add Entry'
                        on_release: app.change_screen('add_entry')
                        IconLeftWidget:
                            icon: 'keyboard'
                    OneLineIconListItem:
                        text: 'Update Entry'
                        on_release: app.change_screen('update_entry')
                        IconLeftWidget:
                            icon: 'notebook'
                    OneLineIconListItem:
                        text: 'View Entries'
                        on_release: app.change_screen('view_entries')
                        IconLeftWidget:
                            icon: 'eye'
                    OneLineIconListItem:
                        text: 'Monthly Summary'
                        on_release: app.change_screen('monthly_summary')
                        IconLeftWidget:
                            icon: 'timetable'
"""


from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

class UltramedikxApp(MDApp):
    theme_cls = ThemeManager()

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.conn = sqlite3.connect('ultramedikx.db')
        self.create_table()
        self.screen = Builder.load_string(screen_helper)
        self.populate_entries_list()
        return self.screen

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    cash_in REAL,
                    pos_cash_in REAL,
                    transfers_cash_in REAL,
                    retainership_cash_in REAL,
                    outstanding_cash_in REAL,
                    expenditure_cash_out REAL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")

    def populate_entries_list(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM entries")
        entries = cursor.fetchall()

        table_box = self.screen.ids.table_box
        table_box.clear_widgets()

        data_table = MDDataTable(
            size_hint=(1, 0.8),
            column_data=[
                ("ID", dp(30)),
                ("Date", dp(30)),
                ("Cash In", dp(30)),
                ("POS Cash In", dp(30)),
                ("Transfers Cash In", dp(30)),
                ("Retainership Cash In", dp(35)),
                ("Outstanding Cash In", dp(35)),
                ("Expenditure Cash Out", dp(35)),
                ("Total", dp(30))
            ],
            row_data=[
                (
                    str(entry[0]),
                    entry[1],
                    f"N{entry[2]:.2f}",
                    f"N{entry[3]:.2f}",
                    f"N{entry[4]:.2f}",
                    f"N{entry[5]:.2f}",
                    f"N{entry[6]:.2f}",
                    f"N{entry[7]:.2f}",
                    f"N{entry[2] + entry[3] + entry[4] + entry[5] + entry[6] - entry[7]:.2f}"
                )
                for entry in entries
            ]
        )

        table_box.add_widget(data_table)

    def change_screen(self, screen_name):
        self.screen.ids.screen_manager.current = screen_name

    def go_home(self):
        self.screen.ids.screen_manager.current = 'home'

    def submit_entry(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO entries (date, cash_in, pos_cash_in, transfers_cash_in, retainership_cash_in, outstanding_cash_in, expenditure_cash_out)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.screen.ids.date.text,
                float(self.screen.ids.cash_in.text or 0),
                float(self.screen.ids.pos_cash_in.text or 0),
                float(self.screen.ids.transfers_cash_in.text or 0),
                float(self.screen.ids.retainership_cash_in.text or 0),
                float(self.screen.ids.outstanding_cash_in.text or 0),
                float(self.screen.ids.expenditure_cash_out.text or 0)
            ))
            self.conn.commit()
            self.populate_entries_list()
            self.change_screen('view_entries')
        except sqlite3.Error as e:
            print(f"An error occurred while submitting the entry: {e}")

    def update_entry(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE entries
                SET date = ?, cash_in = ?, pos_cash_in = ?, transfers_cash_in = ?, retainership_cash_in = ?, outstanding_cash_in = ?, expenditure_cash_out = ?
                WHERE id = ?
            ''', (
                self.screen.ids.update_date.text,
                float(self.screen.ids.update_cash_in.text or 0),
                float(self.screen.ids.update_transfers_cash_in.text or 0),
                float(self.screen.ids.update_retainership_cash_in.text or 0),
                float(self.screen.ids.update_outstanding_cash_in.text or 0),
                float(self.screen.ids.update_expenditure_cash_out.text or 0),
                int(self.screen.ids.entry_id.text)
            ))
            self.conn.commit()
            self.populate_entries_list()
            self.change_screen('view_entries')
        except sqlite3.Error as e:
            print(f"An error occurred while updating the entry: {e}")

    def get_monthly_summary(self):
        try:
            cursor = self.conn.cursor()
            month = self.screen.ids.summary_month.text
            cursor.execute('''
                SELECT 
                    SUM(cash_in),
                    SUM(pos_cash_in),
                    SUM(transfers_cash_in),
                    SUM(retainership_cash_in),
                    SUM(outstanding_cash_in),
                    SUM(expenditure_cash_out)
                FROM entries
                WHERE strftime('%Y-%m', date) = ?
            ''', (month,))
            result = cursor.fetchone()

            if result:
                total_cash_in = result[0] or 0
                total_pos_cash_in = result[1] or 0
                total_transfers_cash_in = result[2] or 0
                total_retainership_cash_in = result[3] or 0
                total_outstanding_cash_in = result[4] or 0
                total_expenditure_cash_out = result[5] or 0
                total_balance = (total_cash_in + total_pos_cash_in + total_transfers_cash_in +
                                 total_retainership_cash_in + total_outstanding_cash_in - total_expenditure_cash_out)

                summary_text = (
                    f"Total Cash In: N{total_cash_in:.2f}\n"
                    f"Total POS Cash In: N{total_pos_cash_in:.2f}\n"
                    f"Total Transfers Cash In: N{total_transfers_cash_in:.2f}\n"
                    f"Total Retainership Cash In: N{total_retainership_cash_in:.2f}\n"
                    f"Total Outstanding Cash In: N{total_outstanding_cash_in:.2f}\n"
                    f"Total Expenditure Cash Out: N{total_expenditure_cash_out:.2f}\n"
                    f"Total Balance: N{total_balance:.2f}"
                )
            else:
                summary_text = "No entries found for this month."

            self.screen.ids.summary_text.text = summary_text
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving the monthly summary: {e}")

    def show_clear_confirmation_dialog(self):
        if not hasattr(self, 'clear_confirmation_dialog'):
            self.clear_confirmation_dialog = MDDialog(
                title="Clear All Entries",
                text="Are you sure you want to clear all entries? This action cannot be undone.",
                buttons=[
                    MDRaisedButton(
                        text="CANCEL",
                        on_release=lambda x: self.clear_confirmation_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="CONFIRM",
                        on_release=lambda x: self.clear_entries()
                    ),
                ],
            )
        self.clear_confirmation_dialog.open()

    def clear_entries(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM entries")
            self.conn.commit()
            self.populate_entries_list()  # Refresh the view to show the empty table
            print("All entries have been cleared.")
            self.clear_confirmation_dialog.dismiss()
        except sqlite3.Error as e:
            print(f"An error occurred while clearing the entries: {e}")


if __name__ == '__main__':
    UltramedikxApp().run()
