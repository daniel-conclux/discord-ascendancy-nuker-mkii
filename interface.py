import customtkinter as ctk
import json
import threading
import subprocess
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.mixer.init()
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("ASC MKII - CONFIGURATIONS")
        self.geometry("600x550")
        self.configure(fg_color="#000000")
        self.attributes("-topmost", True)
        self.parent = parent
        self.entries = {}
        ctk.CTkLabel(self, text="ASCENDANCY N-MKII CONFIG", font=(parent.main_font, 20, "bold"), text_color="#FFFFFF").pack(pady=20)
        try:
            with open("mkii_config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            selfsave = ctk.CTkButton(self, text="SAVE & CLOSE", fg_color="#FFFFFF", text_color="#000000",
                                          hover_color="#CCCCCC", font=(parent.main_font, 14, "bold"), command=self.save_config)
        except Exception:
            config = {"error": "Could not load file"}
            selfsave = ctk.CTkButton(self, text="SAVE & CLOSE", fg_color="#FFFFFF", text_color="#000000",
                                          hover_color="#CCCCCC", font=(parent.main_font, 14, "bold"), command=None)
        for key, value in config.items():
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.pack(fill="x", padx=30, pady=5)
            ctk.CTkLabel(frame, text=f"{key.upper()}:", font=(parent.main_font, 12)).pack(side="left")
            entry = ctk.CTkEntry(frame, fg_color="#000000", border_color="#FFFFFF", border_width=1, font=(parent.main_font, 12))
            entry.insert(0, str(value))
            entry.pack(side="right", expand=True, fill="x", padx=(10, 0))
            self.entries[key] = entry
        self.save_btn = selfsave
        self.save_btn.pack(pady=30)
    def save_config(self):
        new_config = {key: entry.get() for key, entry in self.entries.items()}
        try:
            with open("mkii_config.json", "w", encoding="utf-8") as f: json.dump(new_config, f, indent=4)
            self.destroy()
        except Exception as e:
            pygame.mixer.Sound("SFX\\audio2.mp3").play()
            print(f"Error saving: {e}")

class AscMkiiUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ASC MKII - TRANSCENDENCE EDITION")
        self.geometry("1000x600")
        self.configure(fg_color="#000000")
        self.process = None
        self.log_queue = []
        self.main_font = "Consolas"
        self.settings_window = None
        self.settings_btn = ctk.CTkButton(self, text="☰", width=40, height=40, fg_color="transparent", border_width=1, border_color="#FFFFFF",
                                          font=(self.main_font, 20), command=self.open_settings)
        self.settings_btn.place(x=10, y=10)
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="ASCENDANCY", 
                     font=(self.main_font, 34, "bold"), text_color="#FFFFFF").grid(row=0, column=0, pady=(20, 5))
        ctk.CTkLabel(self, text="Ascendancy N-MKII - Transcendence Edition | Developed by Daniel Conclux", 
                     font=(self.main_font, 12), text_color="#CCCCCC").grid(row=1, column=0, pady=(0, 15))
        pygame.mixer.Sound("SFX\\audio1.mp3").play()
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=0.5, border_color="#FFFFFF")
        self.input_frame.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
        self.guild_input = ctk.CTkEntry(self.input_frame, placeholder_text="01: TARGET GUILD ID", 
                                        fg_color="#000000", text_color="#FFFFFF", border_width=1, border_color="#FFFFFF", 
                                        font=(self.main_font, 14), height=35)
        self.guild_input.pack(pady=(15, 10), padx=20, fill="x")
        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="02: AUTHORIZED USER ID", 
                                       fg_color="#000000", text_color="#FFFFFF", border_width=1, border_color="#FFFFFF", 
                                       font=(self.main_font, 14), height=35)
        self.user_input.pack(pady=(0, 10), padx=20, fill="x")
        self.logo_switch = ctk.CTkSwitch(self.input_frame, text="ENABLE LOGO", text_color="#FFFFFF", progress_color="#CACACA", 
                                         button_color="#FFFFFF", font=(self.main_font, 12))
        self.logo_switch.select()
        self.logo_switch.pack(pady=(5, 15))
        self.terminal = ctk.CTkTextbox(self, fg_color="#000000", text_color="#FFFFFF", 
                                       border_width=1, border_color="#FFFFFF", font=(self.main_font, 12))
        self.terminal.grid(row=3, column=0, padx=30, pady=10, sticky="nsew")
        self.rowconfigure(3, weight=1)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=4, column=0, pady=20)
        self.run_btn = ctk.CTkButton(self.btn_frame, text="INITIATE", fg_color="#FFFFFF", text_color="#000000", 
                                     hover_color="#CCCCCC", font=(self.main_font, 16, "bold"), command=self.start_thread)
        self.run_btn.pack(side="left", padx=10)
        self.stop_btn = ctk.CTkButton(self.btn_frame, text="TERMINATE", fg_color="#FF0000", text_color="#FFFFFF", 
                                      hover_color="#AA0000", font=(self.main_font, 16, "bold"), command=self.stop_sequence, state="disabled")
        self.stop_btn.pack(side="left", padx=10)
        self.update_terminal_loop()
    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
            pygame.mixer.Sound("SFX\\audio3.mp3").play()
        else:
            self.settings_window.focus()
            pygame.mixer.Sound("SFX\\audio3.mp3").play()

    def update_terminal_loop(self):
        if self.log_queue:
            chunk = "".join(self.log_queue)
            self.log_queue.clear()
            self.terminal.insert("end", chunk)
            self.terminal.see("end")
            if len(self.terminal.get("1.0", "end")) > 15000: self.terminal.delete("1.0", "100.0")
        self.after(100, self.update_terminal_loop)

    def stop_sequence(self):
        if self.process:
            self.process.terminate()
            pygame.mixer.Sound("SFX\\audio2.mp3").play()
            self.log_queue.append("\n[!]: Operation cancelled by user\n")
            self.run_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    def start_thread(self):
        if not self.guild_input.get():
            pygame.mixer.Sound("SFX\\audio2.mp3").play()
            self.log_queue.append("[!]: Parameter <Guild ID> is undefined\n")
            return
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        threading.Thread(target=self.run_sequence, daemon=True).start()

    def run_sequence(self):
        try:
            with open("mkii_config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            config["enable_logo"] = "True" if self.logo_switch.get() else "False"
            with open("mkii_config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUNBUFFERED"] = "1"
            self.process = subprocess.Popen(
                [sys.executable, "asc_mkii.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, encoding="utf-8", errors="replace", env=env)
            target_id = self.guild_input.get().strip()
            user_id = self.user_input.get().strip()
            self.process.stdin.write(f"{target_id}\n{user_id}\n")
            self.process.stdin.flush()
            for line in iter(self.process.stdout.readline, ''):
                if line: self.log_queue.append(line)
            self.process.wait()
        except Exception as e:
            pygame.mixer.Sound("SFX\\audio2.mp3").play()
            self.log_queue.append(f"\n[ERROR]: {e}\n")
        finally:
            self.after(0, lambda: self.run_btn.configure(state="normal"))
            self.after(0, lambda: self.stop_btn.configure(state="disabled"))

if __name__ == "__main__":
    app = AscMkiiUI()
    app.mainloop()