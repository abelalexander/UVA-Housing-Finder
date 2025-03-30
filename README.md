# UVA Housing Finder 🏠

Find student housing near your classes at UVA — based on **your schedule**, **walking time**, and **budget**.

## 🚀 Inspiration
As UVA students, we were frustrated with apartment platforms that only consider price and amenities — not where your classes are or how far you'll walk. We created a tool that helps students find housing based on their actual day-to-day life.

## 🧠 What It Does
Students enter their:
- Maximum price
- Number of beds
- Preferred walking time
- School at UVA (Engineering, Data Science, McIntire, or Arts & Sciences)

The app then:
1. Scrapes real-time listings from Apartments.com 🏙️
2. Filters based on price and bedrooms
3. Calculates walking distance to class buildings using Google Maps 🗺️
4. Displays the best-matched apartments in a clean UI

## 🔨 How We Built It
- **Frontend**: HTML/CSS + vanilla JavaScript for the form and result display
- **Backend**: Flask API for handling form input and serving results
- **Web Scraping**: Selenium to extract live data from Apartments.com
- **Distance Calculation**: Google Maps Distance Matrix API to calculate walking times
- **Data Pipeline**: Python handles filtering, formatting, and distance enrichment

## 🧩 Key Files
- `index.html` – Form for user inputs
- `information.html` – Displays dynamic apartment listings
- `app.py` – Flask server that saves form input and serves listings
- `scraper.py` – Scrapes Apartments.com in real-time
- `backend.py` – Filters scraped data and calculates walking times
- `distancePuller.py` – Talks to the Google Maps API

## 🧠 Challenges
- Cross-origin request errors (CORS)
- Merging frontend/backend flows smoothly
- Handling inconsistent and dynamic scraped data
- Managing Google Maps API rate limits

## ✅ Accomplishments
- Live data scraping + real-time distance filtering
- End-to-end stack built in under 48 hours
- Functional MVP tailored to UVA students

## 📚 What We Learned
- Real-world API integration with Google Maps
- Web scraping best practices
- Flask routing and JSON APIs
- Dynamic UI rendering with vanilla JS

## 🔮 What's Next
- Netbadge login to save listings
- Interactive map view with heatmaps
- Mobile-first design
- Deployment to the cloud (e.g. Render or Vercel)

## ⚙️ How to Run Locally
1. Clone the repo
2. Install dependencies:
   ```bash
   pip install flask flask-cors selenium pandas webdriver-manager
   ```
3. Add your Google Maps API key in `distancePuller.py`
4. Run the backend:
   ```bash
   python app.py
   ```
5. In another terminal, run the frontend:
   ```bash
   python -m http.server 3000
   ```
6. Visit: `http://localhost:3000/index.html`

## 📦 Tech Stack
- Python (Flask)
- Selenium
- Google Maps Distance Matrix API
- HTML/CSS/JavaScript
- GitHub

---
