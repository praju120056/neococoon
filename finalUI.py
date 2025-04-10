import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar
import serial
import json

# Serial setup
try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
except Exception as e:
    print(f"Serial error: {e}")
    ser = None

# Send serial command
def send_serial_command(prefix, value):
    if ser and ser.is_open:
        try:
            command = f"{prefix}{value}\n"
            ser.write(command.encode())
        except Exception as e:
            print(f"Error sending: {e}")

# Save settings to file
def save_settings():
    data = {
        "H": meter1.amountusedvar.get(),
        "T": round(temperature_var.get(), 2),
        "P": meter3.amountusedvar.get(),
        "L": meter4.amountusedvar.get(),
        "toggles": {
            "H": toggle1.var.get(),
            "P": toggle3.var.get(),
            "L": toggle4.var.get()
        }
    }
    with open("settings.json", "w") as f:
        json.dump(data, f)

# Restore default settings
def restore_defaults():
    defaults = {
        "H": 50,
        "T": 37.0,
        "P": 25,
        "L": 35,
        "toggles": {"H": "On", "P": "On", "L": "On"}
    }

    meter1.amountusedvar.set(defaults["H"])
    temperature_var.set(defaults["T"])
    meter3.amountusedvar.set(defaults["P"])
    meter4.amountusedvar.set(defaults["L"])

    toggle1.var.set(defaults["toggles"]["H"])
    toggle1.apply_state()

    toggle3.var.set(defaults["toggles"]["P"])
    toggle3.apply_state()

    toggle4.var.set(defaults["toggles"]["L"])
    toggle4.apply_state()

    with open("settings.json", "w") as f:
        json.dump(defaults, f)

# Load settings from file
try:
    with open("settings.json") as f:
        settings = json.load(f)
except FileNotFoundError:
    settings = {
        "H": 50,
        "T": 37.0,
        "P": 25,
        "L": 35,
        "toggles": {"H": "On", "P": "On", "L": "On"}
    }

# Custom toggle button
class CustomToggle(ttk.Frame):
    def __init__(self, master, meter, prefix, style, initial_state="On", **kwargs):
        super().__init__(master, **kwargs)
        self.meter = meter
        self.prefix = prefix
        self.original_style = style

        self.var = StringVar(value=initial_state)
        self.btn = ttk.Checkbutton(
            self,
            textvariable=self.var,
            variable=self.var,
            onvalue="On",
            offvalue="Off",
            bootstyle=style + "-round-toggle",
            command=self.toggle
        )
        self.btn.config(width=40)
        self.btn.pack(fill="both", expand=True, padx=30, pady=30, ipadx=30, ipady=30)

        self.apply_state()

    def toggle(self):
        self.apply_state()

    def apply_state(self):
        if self.var.get() == "Off":
            if self.meter:
                self.meter.configure(interactive=False, bootstyle="secondary")
                send_serial_command(self.prefix, 0)
        else:
            if self.meter:
                self.meter.configure(interactive=True, bootstyle=self.original_style)
                send_serial_command(self.prefix, self.meter.amountusedvar.get())

# Create a meter
def create_meter(master, label, max_val, init_val, unit, style, row, column, prefix, toggle_state):
    container = ttk.Frame(master)
    container.grid(row=row, column=column, padx=20, pady=10, sticky="nsew")
    master.rowconfigure(row, weight=1)
    master.columnconfigure(column, weight=1)

    meter = ttk.Meter(
        container,
        metersize=300,
        amounttotal=max_val,
        amountused=init_val,
        stripethickness=16,
        metertype="semi",
        meterthickness=32,
        subtext=label,
        textright=unit,
        interactive=True,
        bootstyle=style,
        subtextfont='-size 20',
        textfont='-size 36 -weight bold'
    )
    meter.pack(pady=(10, 20), padx=10)

    def enforce_min(meter_var, prefix, min_val):
        def callback(*args):
            val = meter_var.get()
            if val < min_val:
                meter_var.set(min_val)
            else:
                send_serial_command(prefix, val)
        return callback

    meter.amountusedvar.trace_add("write", enforce_min(meter.amountusedvar, prefix, {
            "H": 30,
            "P": 25,
            "L": 25
    }.get(prefix, 0)))

    toggle = CustomToggle(container, meter, prefix, style, initial_state=toggle_state)
    toggle.pack(pady=(0, 10), padx=10)

    return meter, toggle

# Main window
window = ttk.Window(themename="darkly")
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
window.geometry(f"{screenWidth}x{screenHeight}")
window.title("Control Interface")

for r in range(5):
    window.rowconfigure(r, weight=1)
for c in range(4):
    window.columnconfigure(c, weight=1)

label = ttk.Label(window, text="Control Panel", font=("Calibri", 36, "bold"), bootstyle="success")
label.grid(row=0, column=0, columnspan=4, pady=30)

# Create meters and toggles
meter1, toggle1 = create_meter(window, "Humidity", 70, settings["H"], "%", "warning", 1, 0, "H", settings["toggles"].get("H", "On"))
meter3, toggle3 = create_meter(window, "Phototherapy", 100, settings["P"], "%", "primary", 1, 2, "P", settings["toggles"].get("P", "On"))
meter4, toggle4 = create_meter(window, "Light", 100, settings["L"], "%", "light", 1, 3, "L", settings["toggles"].get("L", "On"))

# ---------------- Temperature Slider Section ---------------- #

temp_frame = ttk.Frame(window)
temp_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", pady=20)
window.rowconfigure(2, weight=1)

temp_label = ttk.Label(temp_frame, text="Temperature", font=("Calibri", 20, "bold"), bootstyle="danger")
temp_label.pack(pady=(0, 10))

temperature_var = ttk.DoubleVar(value=settings.get("T", 37.0))

temp_slider = ttk.Scale(
    temp_frame,
    from_=35.0,
    to=38.0,
    variable=temperature_var,
    orient="horizontal",
    length=400,
    bootstyle="danger",
    command=lambda val: send_serial_command("T", max(35.0, round(float(val), 2)))
)
temp_slider.pack(pady=(0, 10))

# Display the temperature value
temperature_display = ttk.Label(temp_frame, text=f"{temperature_var.get():.1f}°C", font=("Calibri", 18), bootstyle="danger")
temperature_display.pack(pady=(0, 10))

# Update label when slider changes
def update_temp_label(*args):
    temperature_display.config(text=f"{temperature_var.get():.1f}°C")

temperature_var.trace_add("write", update_temp_label)

# Buttons: Save, Restore Defaults, Exit
button_frame = ttk.Frame(window)
button_frame.grid(row=4, column=0, columnspan=4, pady=30)

save_btn = ttk.Button(button_frame, text="Save Settings", bootstyle="success-outline", command=save_settings)
save_btn.pack(side="left", padx=30, ipadx=30, ipady=15)

restore_btn = ttk.Button(button_frame, text="Restore Defaults", bootstyle="info-outline", command=restore_defaults)
restore_btn.pack(side="left", padx=30, ipadx=30, ipady=15)

exit_btn = ttk.Button(button_frame, text="Exit to Grafana", bootstyle="danger-outline", command=window.destroy)
exit_btn.pack(side="left", padx=30, ipadx=30, ipady=15)

window.protocol("WM_DELETE_WINDOW", lambda: [save_settings(), ser.close() if ser and ser.is_open else None, window.destroy()])

window.mainloop()
