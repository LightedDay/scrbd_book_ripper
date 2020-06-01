Scribd Book Ripper
============
[![GitHub stars](https://img.shields.io/github/stars/athossampayo/scrbd_book_ripper)](https://github.com/athossampayo/scrbd_book_ripper/stargazers) [![GitHub issues](https://img.shields.io/github/issues/athossampayo/scrbd_book_ripper)](https://github.com/athossampayo/scrbd_book_ripper/issues) [![GitHub forks](https://img.shields.io/github/forks/athossampayo/scrbd_book_ripper)](https://github.com/athossampayo/scrbd_book_ripper/network) [![Version type](https://img.shields.io/badge/version%20type-image-blue)](https://img.shields.io/badge/vers__type-image__version-blue) </br>

### Python script to backup and download scribd books with **premium account**.
#### For any of this type of script to work you need to have a premium account. It can also be a free trial account.
#### This version creates a screenshot of every book page and then generates a PDF file with it. It has the optional ability to generate Searchable Text (as known as OCR) too.
### I have a version of this script that isn't screenshot-based in finishing process, just need to solve one big problem and will release it.
## Table of contents
* [General info](#general-info)
* [Stats](#stats)
* [Dependencies](#dependencies)
* [OCR Setup](#ocr-setup)
* [Script Setup](#script-setup)
* [Disclaimer](#disclaimer)

## General info
This project receives one or more Scribd links and generates a PDF within the books content. It has the option to generate a Searchable PDF too.

## Stats 
֎ _(Will improve in next update!)_ ֎
### Times:
* Downloading a 300 pages book in ± 11,5 minutes in my setup.
* OCR-ed 300 pages in ± 8 minutes.
* Total elapsed time downloading and OCR-ing a 300 pages book: ± 19<5 minutes
### Sizes:
* Non OCR-ed PDF: 11,5MB
* OCR-ed PDF: 9,20MB
##### To updated with more in future. Also accepting other's tests stats.

## Dependencies
This project needs the following python libraries to work:
* selenium
* fpdf
* Pillow
* ocrmypdf _(Optional. Needed for OCR)_
##### For easy installing all at once, use ```pip install requirements.txt```.
* And will need to have Google Chrome installed. You can get it from [here](https://www.google.com/chrome/)

## OCR Setup
If you intend to use the OCR function at the end, you will need to install the following programs, as they are needed for running the ocrmypdf module: </br>
</br>
##### If you enable OCR, the script will generate two PDF files:
- Ended with ```_IMG.pdf``` → Version without OCR
- Ended with ```_OCR.pdf``` → Version with OCR

#### 1.Tesseract-OCR:
For full details on installation, see: https://tesseract-ocr.github.io/tessdoc/Home.html </br>
  * ##### Windows </br>
    You will need to download the installer from: https://github.com/UB-Mannheim/tesseract/wiki </br>
  * ##### Linux </br>
    ```sudo apt install tesseract-ocr``` </br>
    ```sudo apt install libtesseract-dev```

#### 2.Ghostscript
Just download and install from: https://www.ghostscript.com/download/gsdnld.html

## Script Setup
### ChromeDriver
+ Download chromewebdriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Move the driver file to script's root.
### Modify the _config.json_ file:
+ Add your email
+ Add your password
+ "is_list"; if you want to load the links from the _book_list.txt_ file, mark as True
+ "Do_OCR": if you want to automatically execute the OCR process after downloading the file, mark as True
#### Beware! OCR can be time consuming for big books. Test with small ones first so you know how is the output.

### Populate the _book_list.txt_ file (Optional)
+ Just paste one link per line.

## Disclaimer
This project is for **educational purposes** only. It is not advised to use this for any type of copyright or Scribd TOS infringement and **I am not responsible for any misuse of this piece of code.**

## To-Do
- [ ] Correct error when trying to click 'Save book" popup not clicking in time for the screenshot and it appears on the final book
- [ ] Correct line 33 login error and add steps to check if login was really successfull or not (not it interprets as successfull every time)
- [ ] Optimize speed (change every ```time.sleep()``` to ```element_to_be_clickable()``` selenium function
- [ ] Finish and release text-based version of this script
- [ ] Be able to continue already started downloads by checking already downloaded pages


