![Pic](https://cdn.discordapp.com/attachments/1437646588859383889/1448749495616798834/purple-city-4k-pc-poqwfesyy91fbjree8c1.jpg?ex=693c649c&is=693b131c&hm=35d77c079886776d9fe9a465e3deda584c0381cb11175cd8fe557d1264374148)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![OS](https://img.shields.io/badge/OS-Windows%2010%2F11-green)
![License](https://img.shields.io/badge/license-MIT-orange)


[![Download](https://img.shields.io/badge/Download-Latest-blue?style=for-the-badge&logo=github)](https://github.com/unknownperson-vos/Saturn/releases/latest/download/Saturn.zip)

---

# 🌌 **Saturn – Roblox Unowned Group Finder**
Saturn is a **GUI-based** Roblox group scanner designed to find **unowned**, **claimable** Roblox groups with smart rate-limit handling, proxy support, real-time logs, thumbnails, and interactive group info pages.

It uses both the **v1** and **v2** Roblox Groups APIs, dynamically adjusts batch sizes based on success rates, and uses **multi-threading** for maximum scanning speed while keeping the interface smooth.

---

## ⭐ **Features**
- ✔️ Modern **Tkinter GUI**  
- ✔️ Fully automatic **unowned group detection**  
- ✔️ **Smart API batching** (auto increases or decreases load)  
- ✔️ Handles **429 rate limits** gracefully  
- ✔️ **200 – 500 checks/min** *without proxies*  
- ✔️ **1,000 – 5,000 checks/min** *with proxies*  
- ✔️ Multi-threaded scanner (ThreadPoolExecutor)  
- ✔️ Click any group to see:
  - Group name  
  - Thumbnail  
  - Members  
  - Auto-copy claim link  
- ✔️ Proxy loader (`ip:port` or `ip:port:user:pass`)  
- ✔️ Real-time logs  
- ✔️ Internal retry queue for failed IDs  
- ✔️ Auto title updates (“Total Groups Found: X”)  
- ✔️ Clean UI with images, animations, and status indicators  

---

![image](https://cdn.discordapp.com/attachments/1437646588859383889/1448751213440139264/python_GUiABl2hb5.png?ex=693c6635&is=693b14b5&hm=e3012ad2f8c55d9a59d06763d380ac08534f301026715806b217ae68ce606149)

---

## ⚡ **Performance Expectations**

### **Without Proxies**
```
| Threads | Checks/min |
|--------|------------|
| 20–40  | 200–500 |
```

### **With Proxies**
```
| Proxies Loaded | Checks/min |
|----------------|------------|
| 50–150         | 1,000–3,000 |
| 150–300        | 3,000–5,000+ |
```

Performance varies based on:
- proxy quality  
- API behavior  
- automatic batch tuning  
- timeout & latency  

Saturn automatically adjusts:
- increases load on high success rate  
- decreases on errors  
- pauses on consecutive 429s  

---


## 🛠 **Requirements**
You need:

```
Python 3.9+
```

Install packages:

```
pip install -r requirements.txt
```

---

## 🌐 **Proxy Setup (Optional)**

Saturn loads proxies from:

```
proxies/proxies.txt
```

### **Accepted formats**

#### ✔️ Regular proxy
```
123.45.67.89:8080
```

#### ✔️ Proxy with authentication
```
123.45.67.89:8080:user:password
```

### Rules:
- No empty lines  
- No `ip:port` placeholders  
- Automatically converted to:
```
http://user:pass@ip:port
```

If any proxy loads, Saturn automatically uses proxy mode.

---

## ❤️ Contributions
Star this repository !
PRs welcome!

You can contribute:
- UI improvements  
- better proxy rotation  
- code optimizations  
- new group filters
