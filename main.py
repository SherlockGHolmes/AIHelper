from engine import start_engine
from gui import SettingsApp
import threading as th
import time as t
from icon import icon

print("imported")


engine_th = th.Thread(target=start_engine, daemon=True)
icon_th = th.Thread(target=icon.run, daemon=True)

engine_th.start()
icon_th.start()

cord = []

app = SettingsApp()
app.check_queue()
print("started")

app.mainloop()

