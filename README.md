### This repository was made for a technical assignment

# Google Reviews Parser

This is a simple script to parse Google Reviews based on a search string.

## Limitations

This script was written in Pakistan so it may not be usable outside of Pakistan due to different page layout and elements. For example, I did not face any cookie consent popups while writing this.


## Usage

1. Install requirements using `pip install -r requirements.txt`
2. Navigate to the `Parser` directory
3. Run the script using `python parse.py`
4. Enter the search string when prompted
5. Wait for the script to complete running
6. Reviews will be saved in a CSV file named `reviews.csv` in the same directory where you run the script from

## Certificate Errors

If you get a certificate error, you can ignore it. The script will still work. Or you can install the Selenium Wire certifcate to get rid of the error.


## Additional Data

If you need to parse additional data, simply add the corresponding header and the necessary array navigation in the `settings.py` file.
