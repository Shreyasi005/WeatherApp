import tkinter as tk
import requests
from tkinter import messagebox
import geocoder

API_KEY = '1ffdcfa63ce05586564ecefdd297fe3c' 
API_URL = 'https://api.openweathermap.org/data/2.5/weather'

def fetch_weather():
    location = entry_location.get()
    if not location:
        messagebox.showerror("Input Error", "Please enter a location.")
        return

    try:
        response = requests.get(API_URL, params={
            'q': location,
            'appid': API_KEY,
            'units': 'metric'  # Change to 'imperial' for Fahrenheit
        })
        data = response.json()

        if data['cod'] != 200:
            messagebox.showerror("Error", "City not found!")
            return
        
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']

        label_weather.config(text=f"Weather: {weather.capitalize()}")
        label_temperature.config(text=f"Temperature: {temperature}°C")
        label_wind.config(text=f"Wind Speed: {wind_speed} m/s")
        label_humidity.config(text=f"Humidity: {humidity}%")
        
        # Optionally, set a weather icon
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_image = tk.PhotoImage(file=icon_url)  # Or download the icon and display it
        label_icon.config(image=icon_image)
        label_icon.image = icon_image  # Keep reference to avoid garbage collection

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"An error occurred: {e}")

def get_location():
    g = geocoder.ip('me')  # Get location based on IP address
    location = g.city
    entry_location.delete(0, tk.END)
    entry_location.insert(0, location)
    fetch_weather()

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Layout: Create widgets
label_location = tk.Label(root, text="Enter Location:")
label_location.pack()

entry_location = tk.Entry(root, width=30)
entry_location.pack()

button_get_weather = tk.Button(root, text="Get Weather", command=fetch_weather)
button_get_weather.pack()

button_use_gps = tk.Button(root, text="Use GPS Location", command=get_location)
button_use_gps.pack()

label_weather = tk.Label(root, text="Weather: N/A")
label_weather.pack()

label_temperature = tk.Label(root, text="Temperature: N/A")
label_temperature.pack()

label_wind = tk.Label(root, text="Wind Speed: N/A")
label_wind.pack()

label_humidity = tk.Label(root, text="Humidity: N/A")
label_humidity.pack()

label_icon = tk.Label(root)
label_icon.pack()

# Run the app
root.mainloop()
