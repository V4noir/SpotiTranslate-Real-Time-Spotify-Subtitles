# 🎵 SpotiTranslate: Real-Time Spotify Subtitles & Translation

**SpotiTranslate** is a powerful desktop utility that enhances your Spotify experience by fetching real-time synchronized lyrics and displaying them as a sleek, transparent overlay. It doesn't just show the lyrics; it **instantly translates** them into your target language (default: Turkish) using Google Translate.

Perfect for language learners, music enthusiasts, or anyone who wants to understand the meaning of foreign songs while gaming, coding, or working.

---

## ✨ Key Features

* **Live Sync:** Automatically stays in sync with your Spotify playback.
* **Instant Translation:** Powered by the Google Translate engine for on-the-fly lyrics translation.
* **Transparent Overlay:** A borderless, click-through UI that shows only the text, ensuring it doesn't obstruct your workspace.
* **Customizable UI:** Integrated configuration panel to adjust font size and vertical position (Y-Offset).
* **Robust Error Handling:** Built-in safeguards to skip corrupted metadata (like `[ar:Artist]`) or missing lyrics without crashing.
* **Modern Aesthetics:** Built with `CustomTkinter` for a professional dark-themed experience.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.x** installed. You will also need to install the following dependencies:
```bash
pip install requests spotipy deep_translator customtkinter

###Setup Spotify API
Visit the Spotify Developer Dashboard.
Log in and click "Create an App".
Give it a name (e.g., "SpotiTranslate").
Go to "Settings" and find your Client ID and Client Secret.
In the "Redirect URIs" section, add: http://127.0.0.1:8888/callback and save.


Running the App
Clone this repository or download the source code.

Run the main script:

Bash
python main.py
Enter your API credentials in the Settings Window.

Adjust your Font Size and Y-Offset.

Click "Save and Start" and play a song on Spotify!

Technical Details
Lyrics Source: Fetches synchronized lyrics via the LRCLIB API.

Translation: Powered by the deep-translator library.

Session Management: Login tokens are stored locally in a .cache file for seamless re-authentication.


License
This project is licensed under the GNU General Public License v3.0.
Attribution: You must credit the original author (V4noir).
Open Source: Any modifications must remain open-source under the same license.
Non-Commercial: Commercial use is discouraged in the spirit of open-source music tools.

Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
Show your support by giving a ⭐ if you like this project!



