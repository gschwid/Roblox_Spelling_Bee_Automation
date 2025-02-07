# Roblox Spelling Bee Bot.

## Overview
This is a bot created to automate [this](https://www.roblox.com/games/17590362521/10M-Spelling-Bee) Roblox spelling be game. It has a GUI to both start and stop the script, and also gives you updates on the detected words and status of the script. A video of the script working is available [here](https://youtu.be/RN1JVsxGM6k). 

## How does it work?
The bot's functionality consists of three main components:

1) **Turn Detection** – Identifies when it's your turn to spell using visual cues.
2) **Audio Recording** – Captures the spoken word as an audio file.
3) **Speech-to-Text Conversion & Typing** – Converts the recorded audio into text and types it into the game.

### Turn detection. 
The script continuously captures screenshots of the designated spelling area to determine when your character moves into position. Since all players move to the same location, additional verification is required to ensure it's your character.

To achieve this, the bot performs feature matching against a reference image of your character in the correct position. It uses ORB (Oriented FAST and Rotated BRIEF) feature extraction combined with brute-force matching. If a sufficient number of good matches are found, the bot confirms that your character has been detected.

### Audio Recording.
Once the character is detected, the bot records an audio file of the spoken word. This is achieved using PyAudio, which provides functionality for WASAPI (Windows Audio Session API). WASAPI enables loopback recording, allowing the bot to capture system audio directly on Windows machines.

The bot monitors the game for a repeat button that appears when the word has been fully spoken. Upon detecting the button, it stops the recording. If the button does not appear within a set time, the recording times out, assuming the detection was a false match.

### Speech-to-Text Conversion & Typing
The recorded audio file is processed using a retrained version of the Whisper model, fine-tuned on over 400 samples of Roblox Spelling Bee audio to improve transcription accuracy. The Hugging Face library was used for input preprocessing and label tokenization. The retraining process was conducted in a Jupyter Notebook, which is included in the repository [here](https://github.com/gschwid/Roblox_Spelling_Bee_Automation/blob/main/model-tuning/fine_tuned_whisper.ipynb).

Once transcribed, the bot uses PyAutoGUI to automatically type the detected word into the game. When typing the bot has a chance to misinput a letter, allowing for a more human like appereance. 

## How to run this yourself.

This bot should work on most Windows machines. If you're using Windows, follow these steps to set it up:

### 1) Download the compiled program
- Zip file can be found [here](https://drive.google.com/file/d/1n6vo-PFLL8N1JkoMcFGWhvCMTkL2LZyC/view?usp=sharing)
- Download and extract it somewhere on your computer. 
- Open up the folder, you should see the application file, an _internal folder (dont edit this), and a reference picture.

### 2) Prepare a reference image
- You need an image of your Roblox character saved as "reference.png" in this directory, replacing the one showing mine.
- If you're unsure what it should look like, check the example image in the repository.
- Ensure the screenshot only contains your character with minimal background elements for better detection.

### 3) Adjust In-Game Graphics Settings
- Set your Roblox graphics to the lowest setting to improve character detection.
- Lower graphics reduce lighting effects that can blur sharp edges, making recognition more reliable.

### 4) Disable In-Game Music
- Turn off all in-game music to prevent audio interference with the bot’s speech recognition.

### 5) Run the application
- Double click the RobloxSpellingBeeBot executable, this will likely take a little bit to open.
- Have fun!!!
