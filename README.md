# INITIALS LOGO MAKER

This system allows users to create personalized logos by inputting initials, selecting an icon, and customizing the background and text colors. It uses Python libraries such as OpenCV, Pillow, and Tkinter for image processing and graphical user interface (GUI) components.

## Requirements

1. **Python 3.x** – Make sure you have Python installed on your system.

2. **Required Libraries** – This project uses the following Python libraries:
   - `opencv-python`
   - `numpy`
   - `Pillow`
   - `tkinter` (included with Python)
   - `glob`
   - `os`
   - `messagebox`
   
   You can install the required libraries using `pip`:
   ```bash
   pip install opencv-python numpy pillow

***

# How to Use the System

### 1. Launching the Application:
Run the Python script to start the application. A GUI window will open that allows you to customize your logo.

### 2. Logo Customization:
In the GUI, you can customize your logo in the following ways:

- **Enter Initials**:
  - Enter the initials that you want to display in the logo.
  - The initials will be displayed in the center of the logo.

- **Select Font**:
  - Choose a font for the initials from the available system fonts (e.g., Arial, Times New Roman, etc.).

- **Select Icon Source**:
  - **Select Image**: Choose an image (PNG, JPG, or JPEG) from your computer to be used as the logo icon.
  - **Capture Image**: Use your webcam to capture an image that will be used as the logo icon.

- **Select Background Color**:
  - Choose the background color for the logo from the available options (e.g., White, Black, Red, Green, etc.).

- **Select Text Color**:
  - Choose the color for the initials text from the available options.

### 3. Generate the Logo:
After entering the initials and selecting all the options, click the **Generate Logo** button. The logo will be generated based on your inputs and displayed in a new window.

### 4. Saving the Logo:
To save the generated logo, click the "Save" option in the output window.

### 5. Capture Image for Icon:
If you select the **Capture Image** option for the icon, your webcam will open.
- Press **'s'** to save the captured image and use it as the logo icon.
- Press **'q'** to exit without saving the captured image.

### 6. Fonts:
The system automatically detects the fonts available on your system (Windows fonts in `C:/Windows/Fonts/`). You can choose from any of these fonts for your logo text.

***

# Known Issues

- The system currently supports Windows fonts. If using a different operating system, you may need to adjust the font paths.
- The webcam capture for the icon works only on devices with a connected camera.

# Folder Structure
Logo-Maker/
├── main.py          # Python script for the logo maker
├── README.md        # This README file
└── icons/           # Folder for storing captured icons (if necessary)
