# AutoScreenCapture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple yet powerful desktop application for automated, time-interval based screenshot capturing, built with Python and Tkinter.


## Features

-   **User-Friendly Interface:** Clean and intuitive GUI built with `tkinter` and modern `ttk` widgets.
-   **Custom Save Location:** Easily browse and select any folder on your computer to save the screenshots.
-   **Adjustable Interval:** Use a simple slider to set the time interval between captures (from 5 to 300 seconds).
-   **Start/Stop Control:** Full control to start and stop the automated capture process at any time.
-   **Non-Blocking Operation:** The capture process runs in a separate thread, so the application remains responsive.
-   **Live Status Updates:** See the current status, the total number of screenshots taken, and the name of the last file saved.
-   **Instant Test Screenshot:** Take a single, immediate screenshot to test your settings without starting the full process.
-   **Image Preview:** A small preview of the last screenshot taken is displayed directly in the app.
-   **Timestamped Filenames:** Screenshots are automatically saved with a `YYYYMMDD_HHMMSS` timestamp for easy organization.
-   **Dependency Checks:** The application checks for required libraries on startup and provides helpful error messages if they are missing.

## Requirements

-   Python 3.x
-   The following Python libraries:
    -   `Pillow`
    -   `pyautogui`

## Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/azario0/AutoScreenCapture.git
    cd AutoScreenCapture
    ```

2.  **Install the required packages:**
    It's recommended to use a virtual environment.
    ```sh
    # Create and activate a virtual environment (optional but recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install dependencies
    pip install Pillow pyautogui
    ```

## Usage

1.  Run the application from your terminal:
    ```sh
    python app.py
    ```

2.  **Browse for a Folder:** Click the "Browse" button to select the directory where you want to save your screenshots. The default is your Desktop.

3.  **Set the Interval:** Drag the slider to set the time in seconds between each screenshot.

4.  **Start Capturing:** Click the "▶ Start Capture" button. The application will now take a screenshot of your entire screen at the interval you specified.

5.  **Stop Capturing:** Click the "⏹ Stop Capture" button to end the process.

6.  **Test Screenshot:** Click the "📷 Test Screenshot" button at any time to take a single screenshot and confirm everything is working correctly.

## How It Works

-   **GUI:** The graphical user interface is built using Python's standard `tkinter` library, with the `ttk` module for a more modern look and feel.
-   **Screenshotting:** The core screenshot functionality is handled by the `pyautogui` library, which can programmatically control the mouse and keyboard as well as capture the screen.
-   **Concurrency:** To prevent the GUI from freezing while waiting for the next screenshot interval, the capture loop runs in a separate `threading.Thread`. This ensures the application remains responsive at all times.
-   **Image Handling:** The `Pillow` library is used to process the captured screenshot and generate a resized thumbnail for the preview panel.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/azario0/AutoScreenCapture/issues).

## License

This project is licensed under the MIT License.


