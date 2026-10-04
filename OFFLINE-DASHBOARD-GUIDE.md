# Guide to Running the Dashboard Without Internet (Offline Mode)

## Method 1: Direct Run (requires downloading Chart.js)

### Step 1: Download Chart.js

1. Download the Chart.js file from one of the addresses below:
   - **CDN Link**: https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js
   - **Or from the official site**: https://www.chartjs.org/docs/latest/getting-started/installation.html

2. Save the downloaded file in the same folder where `dashboard-html-demo.html` is located and name it `chart.umd.min.js`.

### Step 2: Modify the HTML File

Open the `dashboard-html-demo.html` file and find the following line:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

Change it to this:

```html
<script src="./chart.umd.min.js"></script>
```

### Step 3: Run

1. Disconnect your internet connection
2. Double-click the `dashboard-html-demo.html` file
3. The Dashboard opens in the browser and works without internet

---

## Method 2: Run with Fallback (if Chart.js has not been downloaded)

The `dashboard-html-demo.html` file already has a fallback mechanism that uses a simple version if the CDN is unavailable.

**Note**: This method has limited functionality and charts may not display properly.

---

## Method 3: Run Using a Local Server (recommended)

### Using Python (if installed):

1. In Command Prompt or PowerShell, go to the file's folder:
```bash
cd "C:\Users\asus\Documents\companies\ithub\AI\products\clones\fidps\FIDPS---Intelligent-Formation-Integrity-damage-prevention-system-"
```

2. Start a local server:

**Python 3:**
```bash
python -m http.server 8000
```

**Python 2:**
```bash
python -m SimpleHTTPServer 8000
```

3. Open the browser and go to the following address:
```
http://localhost:8000/dashboard-html-demo.html
```

### Using Node.js (if installed):

1. Install http-server:
```bash
npm install -g http-server
```

2. Run in the file's folder:
```bash
http-server -p 8000
```

3. Open in the browser:
```
http://localhost:8000/dashboard-html-demo.html
```

---

## Method 4: Create a Fully Standalone Version

To create a fully standalone version with no external dependencies:

### Step 1: Download Chart.js

Download from this link:
```
https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js
```

### Step 2: Embed Directly in HTML

You can place the contents of the `chart.umd.min.js` file directly in the HTML file (this makes the file large but fully standalone).

---

## Important Notes:

1. **Best method**: Method 1 (download Chart.js and use locally)
2. **Quick way**: use a local server (Method 3) - it works even without internet if Chart.js has already been downloaded
3. **Save Dashboard**: the "Save Dashboard" button at the top of the page saves the data to a JSON file and also in the browser's localStorage
4. **Data Persistence**: data saved in localStorage persists even after closing the browser

---

## Required File Structure:

```
FIDPS---Intelligent-Formation-Integrity-damage-prevention-system-/
├── dashboard-html-demo.html    (main Dashboard file)
├── chart.umd.min.js            (Chart.js file - must be downloaded)
└── OFFLINE-DASHBOARD-GUIDE.md  (this guide)
```

---

## Quick Start Guide:

1. **Download Chart.js:**
   - Open the browser and go to this address: `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`
   - Right-click → Save As → save the file in the same folder as `dashboard-html-demo.html`

2. **Modify the HTML file:**
   - Open `dashboard-html-demo.html` with Notepad or VS Code
   - Find lines 8-20, which relate to the Chart.js script
   - Instead of the CDN link, use `./chart.umd.min.js`

3. **Run:**
   - Double-click the `dashboard-html-demo.html` file
   - The Dashboard runs without needing internet!

---

## Support:

If a problem occurs, check:
- ✅ Is the `chart.umd.min.js` file in the same folder as the HTML?
- ✅ Is the file path in the `<script>` tag correct?
- ✅ Does the browser Console (F12) show any error?
