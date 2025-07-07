
# 👶 NeoCocoon: Smart Baby Incubator System

A smart, affordable, and remotely monitorable **baby incubator system** designed to improve neonatal care accessibility. Built with embedded hardware integration and a web-based monitoring dashboard, NeoCocoon offers real-time vitals tracking and environmental control for premature and at-risk infants.

---

## 📌 Features

✅ Real-time monitoring of **temperature**, **humidity**, **phototherapy**, and **white light levels**  
✅ User interface built with **Tkinter + TTKBootstrap** for Raspberry Pi touchscreen control  
✅ Serial communication with onboard sensors and actuators via **Raspberry Pi Pico**  
✅ Data visualization and control feedback via an integrated web dashboard (planned)  
✅ Scalable architecture for hospital-grade or home setups  

---

## 📂 Project Structure


├── UI/  
│   ├── neococoon_ui.py         # Main GUI code for Raspberry Pi interface  
│   ├── assets/                 # Icons, images, and GUI assets  
│   └── requirements.txt        # Python dependencies  
├── Embedded/  
│   ├── sensor_code.ino         # Microcontroller firmware (Arduino/C++)  
│   └── protocol_specs.txt      # Communication protocol documentation  
├── Dashboard/  
│   ├── web_dashboard_plan.md   # Planned web dashboard implementation notes  
├── README.md                   # Project documentation  
└── LICENSE  

---

## ⚙️ How It Works

1. **Sensors connected to Raspberry Pi Pico** measure environmental vitals.
2. Data is transmitted via **serial communication** to the Raspberry Pi.
3. **Raspberry Pi UI (Tkinter + TTKBootstrap)** visualizes sensor values and allows adjusting light levels and temperature settings.
4. Control commands are sent back via serial to adjust actuators like heaters, humidifiers, and phototherapy lamps.
5. (Planned) Data can be logged and remotely monitored via a **web dashboard**.

---

## 🚀 Getting Started

### 📥 Clone the Repository


git clone https://github.com/praju120056/neococoon.git  
cd neococoon  


### 🛠️ Install Dependencies (for UI)

cd UI  
pip install -r requirements.txt


### ▶️ Run the Raspberry Pi UI


python neo_ui.py


---

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/1a2a5ff6-8646-4832-aba0-2f2acda20b37)


---

## 🎯 What I Learned

- Serial communication protocols between microcontrollers and Raspberry Pi
- GUI design using **Tkinter** and **TTKBootstrap**
- Real-time data visualization and control in embedded systems
- Hardware interfacing and actuator management
- Planning scalable IoT medical systems

---

## 📌 To-Do (Roadmap)

- [ ] Complete web-based monitoring dashboard (React/Flask + Grafana)
- [ ] Integrate database storage for vitals logging
- [ ] Add alert system (email/SMS) for critical conditions
- [ ] Finalize enclosure design for safe incubator housing

---

## 📚 References

- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [TTKBootstrap Docs](https://ttkbootstrap.readthedocs.io/en/latest/)
- [Serial Communication with PySerial](https://pyserial.readthedocs.io/en/latest/)

---

## 🧑‍💻 Author

**Prajakth N Kumar**  
[GitHub](https://github.com/praju120056) | [LinkedIn](https://www.linkedin.com/in/prajakth-n-kumar-0092902a6/)

---

## 📜 License

This project is licensed under the **MIT License** — free for personal and educational use.

---

⭐️ If you found this interesting, give it a star and feel free to contribute!
