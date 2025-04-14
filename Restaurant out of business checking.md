To check if a restaurant is permanently closed (i.e., out of business) using Python, you generally need to rely on **external data sources** like:

- Google Places API
- Yelp Fusion API
- Web scraping (if APIs aren't available)
- Business directories (local or global)

Here’s a breakdown of how to approach it:

---

### ✅ **1. Using Google Places API (Most Reliable)**

Google Places API can return a field `business_status` which may be:

- `OPERATIONAL`
- `CLOSED_TEMPORARILY`
- `CLOSED_PERMANENTLY`

#### **Install and Setup**
```bash
pip install googlemaps
```

#### **Code Example**
```python
import googlemaps

gmaps = googlemaps.Client(key='YOUR_API_KEY')

place = gmaps.find_place(
    input="Joe's Pizza, New York",
    input_type="textquery",
    fields=["place_id", "business_status", "name", "formatted_address"]
)

if place["candidates"]:
    status = place["candidates"][0].get("business_status", "UNKNOWN")
    print(f"Business status: {status}")
else:
    print("Restaurant not found.")
```

---

### ✅ **2. Using Yelp Fusion API**

Yelp also has business data, including whether a business is open or not.

[Get an API key](https://www.yelp.com/developers/documentation/v3/get_started), then:

```python
import requests

api_key = 'YOUR_YELP_API_KEY'
headers = {'Authorization': f'Bearer {api_key}'}

params = {'term': "Joe's Pizza", 'location': 'New York'}
response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)

data = response.json()
if data["businesses"]:
    business = data["businesses"][0]
    is_closed = business.get("is_closed", None)
    print(f"Closed: {is_closed}")
else:
    print("No business found.")
```

---

### ✅ **3. (Alternative) Web Scraping**  
As a last resort, you can scrape business listings like Google Maps, Yelp, or TripAdvisor — but they may block bots and violate TOS.

---

### ✅ Which is best?
- Use **Google Places API** if you need detailed and reliable info, including permanently closed status.
- Use **Yelp API** if you’re focused on North America and care about reviews + status.
