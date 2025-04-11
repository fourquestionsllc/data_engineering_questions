Looking for **free (or generous free-tier)** alternatives to Google Maps to search restaurants by latitude and longitude in Python, here are some solid options:

---

## ✅ 1. **OpenStreetMap + Overpass API** (Free & Open Source)

You can query restaurants using lat/lon and radius via Overpass API, which runs on OpenStreetMap data.

### 🔧 Sample Python Code:
```python
import requests

def search_osm_restaurants(lat, lon, radius=1000):
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="restaurant"](around:{radius},{lat},{lon});
      way["amenity"="restaurant"](around:{radius},{lat},{lon});
      relation["amenity"="restaurant"](around:{radius},{lat},{lon});
    );
    out center;
    """

    response = requests.post(overpass_url, data={"data": query})
    data = response.json()

    restaurants = []
    for element in data['elements']:
        name = element.get('tags', {}).get('name', 'Unnamed')
        lat = element.get('lat') or element.get('center', {}).get('lat')
        lon = element.get('lon') or element.get('center', {}).get('lon')
        restaurants.append({"name": name, "lat": lat, "lon": lon})

    return restaurants

# Example usage:
if __name__ == "__main__":
    lat, lon = 40.748817, -73.985428  # Example: New York City
    results = search_osm_restaurants(lat, lon)
    for idx, r in enumerate(results, 1):
        print(f"{idx}. {r['name']} at ({r['lat']}, {r['lon']})")
```

✅ **No API key required**, fully free.

---

## ✅ 2. **Foursquare Places API (Free tier available)**

Foursquare offers a generous free tier (limited daily calls) for POI search.

### 🔧 Use case:
- Requires API key
- More structured data than OpenStreetMap

You can sign up for free: [https://developer.foursquare.com](https://developer.foursquare.com)

---

## ✅ 3. **OpenCage Geocoder + Overpass** (for full geocoding + POI)
- OpenCage is mostly for geocoding, but often used in combination with Overpass.
- Limited free tier (2,500 requests/day)

---

## Summary

| API | Free? | Key Required? | Supports Restaurant Search by Lat/Lon? |
|------|-------|----------------|----------------------------------------|
| **OpenStreetMap + Overpass** | ✅ Yes | ❌ No | ✅ Yes |
| **Foursquare Places API** | ✅ Free Tier | ✅ Yes | ✅ Yes |
| **Google Maps** | ⚠️ Limited Free Tier | ✅ Yes | ✅ Yes |
| **OpenCage + Overpass** | ✅ Free Tier | ✅ Yes | ✅ Via Overpass |

---

Would you like me to wrap this into a **Streamlit app**, chatbot, or REST API for you to deploy?
