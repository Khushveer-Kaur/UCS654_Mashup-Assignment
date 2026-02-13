# UCS654
## Name- Khushveer Kaur
## Roll number- 102303327
# YouTube Mashup Generator

This project is developed as part of the Mashup Assignment.

It consists of two parts:

1. Command Line Python Program
2. Web Service for Mashup Generation

------------------------------------------------------------

## Program 1 – Command Line Mashup Generator

### Objective:
This program:
- Downloads N YouTube videos of a given singer
- Converts videos to audio
- Cuts first Y seconds from each audio
- Merges all trimmed audios
- Produces one final mashup file

### How to Run:

Open command prompt inside project folder and run:

`python <RollNumber>.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFileName>`

Example:

`python 102303327.py "Sharry Maan" 12 25 mashup.mp3`

### Conditions:

- NumberOfVideos must be greater than 10
- AudioDuration must be greater than 20 seconds
- Proper argument validation implemented
- Exception handling included

### Output:

A merged MP3 mashup file will be generated in the same directory.

------------------------------------------------------------

## Program 2 – Web Service

### Objective:
This web service allows a user to:
- Enter Singer Name
- Enter Number of Videos
- Enter Duration
- Enter Email ID

The system:
- Generates the mashup
- Creates a ZIP file
- Sends it to the user's email

### How to Run:

Step 1: Install dependencies

`pip install -r requirements.txt`

Step 2: Run the Flask server

`python app.py`

Step 3: Open browser and go to:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

Step 4: Fill the form and submit.

The mashup ZIP file will be sent to the provided email.

------------------------------------------------------------

## Technologies Used

- Python
- Flask
- yt-dlp
- FFmpeg
- SMTP (Email sending)

------------------------------------------------------------

## Requirements

- Python 3.10+
- FFmpeg installed and added to system PATH
- Gmail App Password enabled for email sending

------------------------------------------------------------

## Notes

- Downloads folder is created automatically.
- Temporary files are cleaned after execution.
- Email validation is implemented.
- Input validation is implemented.

------------------------------------------------------------


