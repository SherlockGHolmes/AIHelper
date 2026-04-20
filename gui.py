import customtkinter as ctk
from CTkMessagebox import CTkMessagebox as ctkmsgbox
import json
from shared import task_queue

with open("settings.json", "r") as f:
    data = json.load(f)
ctk.set_appearance_mode(data["mode"])
ctk.set_default_color_theme("dark-blue")

class SettingsApp(ctk.CTk):
    def __init__(self):
        super().__init__()



        with open("settings.json", "r") as f:
            self.data = json.load(f)

        #basic settings
        self.title("Beállítások")
        self.geometry("400x300")
        self.attributes("-topmost", True)
        self.app_instance = None
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.withdraw()

        #api
        self.api_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.api_frame.pack(pady=20, padx=20, fill="x") 

        self.api_label = ctk.CTkLabel(self.api_frame, text="Groq API Kulcs:")
        self.api_label.pack(side="left", pady=10, padx=10)

        self.api_entry = ctk.CTkEntry(self.api_frame, width=300)
        self.api_entry.pack(side="left", pady=10)
        
        self.api_button = ctk.CTkButton(self.api_frame, text="Mentés", command=self.save_apikey)
        self.api_button.pack(side="left", pady=10, padx=10)

        #change mode
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=20, padx=20, fill="x")

        self.mode_label = ctk.CTkLabel(self.mode_frame, text="Megjelenési mód:")
        self.mode_label.pack(side="left", pady=10, padx=10)

        self.mode_option = ctk.CTkSwitch(self.mode_frame, text="", command=self.switch_mode)
        self.mode_option.pack(side="left", pady=10, padx=10)
        
        #auto paste
        self.paste_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.paste_frame.pack(pady=20, padx=20, fill="x")

        self.paste_label = ctk.CTkLabel(self.paste_frame, text="Autómatikus beillesztés")
        self.paste_label.pack(side="left", pady="10", padx="10")

        self.paste_option = ctk.CTkSwitch(self.paste_frame, text="", command=self.swith_paste)
        self.paste_option.pack(side="left", pady="10", padx="10")

        #show result
        self.note_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.note_frame.pack(pady=20, padx=20, fill="x")

        self.note_label = ctk.CTkLabel(self.note_frame, text="Értesítés az eredményről")
        self.note_label.pack(side="left", pady="10", padx="10")

        self.note_switch = ctk.CTkSwitch(self.note_frame, text="", command=self.switch_note)
        self.note_switch.pack(side="left", pady="10", padx="10")


        #apply swithces
        self.apply_mode()

    def hide_window(self):
        self.withdraw()

    def save_apikey(self):

        apikey=self.api_entry.get()
        if len(apikey.strip()) == 56:
            with open(".env", "w") as f:
                f.write(f"API_KEY={apikey.strip()}")
            ctkmsgbox(title="Siker", message="API kulcs sikeresen elmentve!\nIndítsd újra a programot.", icon="check")
            
        else:
            ctkmsgbox(title="Hiba", message="Vmi hülyeséget adtál meg,\n az iq szinted nem haladja meg a szobahőmérsékletet sem.", icon="cancel")
    
    def switch_mode(self):

        ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")
        self.change_data("mode", ctk.get_appearance_mode())

    
    def swith_paste(self):
        with open("settings.json", "r") as f:
            data = json.load(f)
        paste = data["auto_paste"]

        paste_new = False if paste else True

        self.change_data("auto_paste", paste_new)
        
    def switch_note(self):
        note = self.data["note"]
        note_new = False if note else True
        self.change_data("note", note_new)
    
    def change_data(self, key, value):
        filepath = "settings.json"

        with open(filepath, "r") as f:
            data = json.load(f)

        data[key] = value

        with open(filepath, "w") as f:
            json.dump(data, f)

    def apply_mode(self):
            mode = self.data["mode"]
            paste = self.data["auto_paste"]
            note = self.data["note"]    

            if mode == "Dark":
                self.mode_option.select()
            else:
                self.mode_option.deselect()
            
            if paste:
                self.paste_option.select()
            else:
                self.paste_option.deselect()
            if note:
                self.note_switch.select()
            else:
                self.note_switch.deselect()

    def check_queue(self):
        try:
            task = task_queue.get_nowait()
            if task == "open":
                self.open_window()
        except:
            pass
        self.after(100, self.check_queue)

    def open_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

if __name__ == "__main__":
    app = SettingsApp()
    app.mainloop()