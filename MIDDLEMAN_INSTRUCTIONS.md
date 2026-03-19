# ️ Middleman (Scanner Laptop) Instructions

You are running the **QR code scanner station**. Your job is to scan QR codes that scouters hold up on their phones and push the data to the server automatically.

**You need: a laptop or tablet with a camera and WiFi.**

---

## Step 1 — Connect to WiFi

Connect to a network that has internet access (venue WiFi, hotspot, etc.). You just need to reach `scout.thaliathenerd.dev`.

---

## Step 2 — Open the Scanner

Open any browser (Chrome or Firefox recommended) and go to:

```
https://scout.thaliathenerd.dev/scanner.html
```

> **Tip:** Bookmark this before the event so you can open it fast.

---

## Step 3 — Allow Camera Access

When the browser asks for camera permission, tap **Allow**. The scanner will open your camera automatically.

---

## Step 4 — Scan QR Codes

1. A scouter holds their phone with a QR code up to your camera
2. Point the camera at the QR code — it scans automatically, no button needed
3. You'll see a **green flash** and a toast notification like:
   -  Match 4, Team 1234
   -  Pit Data: Team 5678
4. The scanner is ready for the next one immediately

### What the status bar means

| Status | Meaning |
|---|---|
|  Ready to scan... | Good, camera is on |
|   Match X, Team Y | Data saved to server |
|  API Error | Server unreachable, see troubleshooting |

### Counters at the bottom
- **Scanned** — total QR codes detected
- **Success** — data saved to server 
- **Errors** — failed submissions 

---

## Step 5 — Check the Dashboard

Open a second tab to monitor incoming data:

```
https://scout.thaliathenerd.dev:8501
```

This is the Streamlit dashboard — you can see all submitted match and pit data live.

---

## Troubleshooting

**Camera won't start:**
- Make sure you're using HTTPS (not HTTP) — browsers block camera on plain HTTP
- Try a different browser (Chrome works best)
- Check that no other app is using the camera

**API Error / data not saving:**
- Check your WiFi — you need internet access to reach the server
- Try reloading the page
- Check the dashboard to confirm whether data actually got through (sometimes the error clears)

**QR code not scanning:**
- Make sure the scouter's screen brightness is turned up
- Hold steady — don't move the phone
- The QR code needs to fill most of the camera box
