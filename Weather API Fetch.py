import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from requests import HTTPError, RequestException


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WeatherApp")
        self.setGeometry(600, 400, 500, 300)

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
                padding: 5px;
                border: 2px solid gray;
                border-radius: 10px;
                height: 50px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 85px;
                font-weight: bold;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Apple Color emoji;
            }
            QLabel#description_label{
                font-size: 50px;
                font-weight: bold;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "010c63a6dd6ded3ae93c8bc67b1f7e4f"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nCheck Input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API")
                case 403:
                    self.display_error("Access Denied:\nForbidden")
                case 404:
                    self.display_error("Not Found:\nCity Not Found")
                case 500:
                    self.display_error("Internal Error:\nTry Later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid Response")
                case 503:
                    self.display_error("Service Unavailable:\nServer Down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo Server Response")
                case _:
                    self.display_error("HTTP Error Occurred")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f" Request Error:\n{req_error}")


    def display_error(self, message):
        self.city_input.clear()

        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)

        self.emoji_label.setText("")
        self.description_label.setText("")

    def display_weather(self, data):
        self.city_input.clear()

        temperature_k = data["main"]["temp"]
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        capitalized_description = weather_description.title()

        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        self.description_label.setText(capitalized_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        match weather_id:
            case 200 | 201 | 202 | 230 | 231 | 232:  # Thunderstorm with rain
                return "⛈️"
            case 210 | 211 | 212 | 221:  # Thunderstorm
                return "🌩️"
            case 300 | 301 | 302 | 310 | 311 | 312 | 313 | 314 | 321:  # Drizzle
                return "🌧️"
            case 500 | 501:  # Light rain / Moderate rain
                return "🌦️"
            case 502 | 503 | 504:  # Heavy rain
                return "🌧️"
            case 511:  # Freezing rain
                return "🧊"
            case 520 | 521 | 522 | 531:  # Showers
                return "🌦️"
            case 600 | 601:  # Light snow / Snow
                return "🌨️"
            case 602:  # Heavy snow
                return "❄️"
            case 611 | 612 | 613:  # Sleet
                return "🌨️"
            case 615 | 616:  # Rain and snow
                return "🌧️❄️"
            case 620 | 621 | 622:  # Snow showers
                return "🌨️"
            case 701 | 741:  # Mist / Fog
                return "🌫️"
            case 711:  # Smoke
                return "🔥"
            case 721:  # Haze
                return "🌫️"
            case 731 | 751 | 761 | 762:  # Dust / Sand / Ash
                return "🏜️"
            case 771:  # Squalls
                return "💨"
            case 781:  # Tornado
                return "🌪️"
            case 800:  # Clear sky
                return "☀️"
            case 801:  # Few clouds
                return "🌤️"
            case 802:  # Scattered clouds
                return "⛅"
            case 803:  # Broken clouds
                return "☁️"
            case 804:  # Overcast clouds
                return "☁️☁️"
            case _:
                return "❓"  # Unknown condition


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Weather_app = WeatherApp()
    Weather_app.show()
    sys.exit(app.exec())