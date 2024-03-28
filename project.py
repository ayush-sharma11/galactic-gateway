import streamlit as st
import requests
import webbrowser

def read_api_key():
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
    return api_key

API_KEY = read_api_key()


def main():
    st.title("Galactic Gateway")
    st.subheader("Journey Through the Universe with NASA API and Python")

    page = st.sidebar.radio("Navigation", ["Home", "Astronomy Picture Of The Day", "Mars Pictures", "Earth Image", "Custom Search"])

    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1475274047050-1d0c0975c63e?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    if page == "Home":
        st.header("Hello!")
        st.subheader("Choose any API endpoint from the sidebar.")
    
    elif page == "Astronomy Picture Of The Day":
        st.header("APOD - Astronomy Picture Of The Day")
        apod()
    
    elif page == "Mars Pictures":
        st.header("Mars Pictures captured by Curiousity Rover")
        num = st.number_input("How many pictures do you want to see: ", min_value=0, max_value=20)
        st.write("Max limit is 20")
        mars_pictures(num)
    
    elif page == "Earth Image":
        st.header("This retrieves the date-times and asset names for closest available imagery for a supplied location and date.")
        lat = st.number_input("Latitude: ", step=0.1)
        lon = st.number_input("Longitude: ", step=0.1)
        date = st.text_input("Date", "")
        st.write("In YYYY-MM-DD format only!")

        earth_image(lon, lat, date)
    
    elif page == "Custom Search":
        st.header("Custom Search")
        custom_search()
    

def apod():
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}")
    if response.status_code == 200:
        data = response.json()
        url = data["url"]
        description = data["explanation"]

        st.image(url)
        st.write(description)
    else:
        st.error("Failed to fetch Astronomy Picture of the Day. Please check your API key.")

def custom_search():
    query = st.text_input("What would you like to see", "")
    number = st.number_input("And how many photos", min_value=1, max_value=10, step=1)

    number = int(number)
    st.write("At maximum, only top 10 images will be displayed")
    
    if query and number <= 10:
        url = f"http://images-api.nasa.gov/search?q={query}"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            image_urls = []
            for item in data.get('collection', {}).get('items', []):
                if item.get('links'):
                    image_urls.extend(link['href'] for link in item['links'] if link.get('href'))

            for i in range(number):
                st.image(image_urls[i])

def mars_pictures(num):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        image_urls = []
        for photo in data.get("photos", [])[:num]:
            image_urls.append(photo['img_src'])

        for i in range(min(num, len(image_urls))):
            st.image(image_urls[i])

def earth_image(lon, lat, date):
    lon= str(lon)
    lat = str(lat)

    url = f"https://api.nasa.gov/planetary/earth/imagery?lon={lon}&lat={lat}&date={date}&&&dim=0.10&api_key={API_KEY}"

    # webbrowser.open(url)

    response = requests.get(url)
    if response.status_code == 200:
        st.image(url)

def apod_response():
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}")
    return response.status_code

def mars_pictures_response():
    response = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={API_KEY}")
    return response.status_code

def earth_image_response():
    response = requests.get(f"https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date=2014-02-01&api_key={API_KEY}")
    return response.status_code

    
if __name__ == "__main__":
    main()
