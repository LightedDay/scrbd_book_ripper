import base
from time import sleep
import os, re, json, datetime
import ocrmypdf

start_time = datetime.datetime.now()    #log inicial time

#function for checking and creating the dir for the temporary book images
def check_dir(book_id,path):
    if os.path.exists(os.path.join(path,book_id,'')) == False:
        os.makedirs(os.path.join(path,book_id,''))

#function for reading book_list.txt if set so on config.json
def open_book_list(book_list):
    if book_list == "True":
        with open('book_list.txt', 'r') as f:
            bk_list = f.readlines()
            f.close()
            #checks if any of the URLS aren't right
            for item in bk_list:
                if 'scribd.com' not in item:
                    print("\nCheck your 'book_list.txt' for invalid links. If your are not willing to use a URL list, please change 'is_list' in 'config.json' to 'False'\n\n")
                    print('Problematic item: "{item}"'.format(item=item))
                    exit()
        return bk_list
    elif book_list == "False":
        bk_url = input("paste your Scribd book URL here.\n")
        bk_list = []
        bk_list.append(bk_url)
        #checks if its really a scribd URL
        if bk_url == "" or bk_url == " " or 'scribd.com' not in bk_url:
            print('\nInvalid URL added. Closing script...\n')
            exit()
        return bk_list

#runs the ocr if set so on config.json
def ocr(book_title):
    if config['Do_OCR'] == "True":
        book_title = book_title + '_IMG'
        ocrmypdf.ocr(book_title+'.pdf', book_title+"_OCR.pdf", use_threads=True)
    else:
        pass

#function to replace any forbidden filename characters so later seçenium doesnt have problem saving screenshot files
def book_title_cleaning(book_title):
    reserved = ['<','>',':','"','/','\\','|','?','*']
    book_title_cleaned = ""
    for i in range(len(book_title)):
        if book_title[i] in reserved:
            book_title_cleaned += " "
        else:
            book_title_cleaned += book_title[i]
    return book_title_cleaned

#reads the config.json    

json_file = open('./config.json')
config = json.load(json_file)
email = config["email"]
password = config["password"]
book_list = config["is_list"]

#checks for valid email
if email == '' or email == ' ' or email == None:
    print("Please check email in config.json")
    
#checks for valid password
if password == '' or password == ' ' or password == None:
    print("Please check email in config.json")

book_urls = open_book_list(book_list)



pre_checks = base.pre_checks()    #sets pre_checks class from base.py file
screenshots = base.Screenshots()  #sets Screenshots class from base.py file
pdf_gen = base.PDF_Gen()          #sets PDF_Gen class from base.py file

#itaration over the urls
for url in book_urls:
    #if url is not the main book page, edits it to be
    if '/read/' in url:
        url = url.replace('/read/', '/book/')
    path = os.getcwd()      #user path
    book_id = re.findall(r'\/\d+\/', url)[0].replace('/', '')   #find book_id to use later
    check_dir(book_id, path)
    acess = list(pre_checks.read_link(url))     #receives book_url and book_ttle
    read_url = acess[0]
    book_title = acess[1]
    book_title_cleaning(book_title)             #cleaning any forbidden filename characters
    screenshots.screenshot(read_url, book_title, email, password, book_id)  #whole login and screenshot process. Check
                                                                            #base.py for details
    pdf_gen.main(book_title, book_id)           #Whole images pdf creation. Check base.py for details 
    end_dl_time = datetime.datetime.now()
    elapsed_time = end_dl_time - start_time     #elapsed time for screenshoting
    print('Elapsed time for screenshot this book: {time}'.format(time=elapsed_time))
    ocr(book_title)
    elapsed_ocr = datetime.datetime.now()
    elapsed_ocr = elapsed_ocr - end_dl_time     #elapsed time for ocr-ing
    total_elapsed = datetime.datetime.now()
    total_elapsed = total_elapsed - start_time  #total elapsed time
    print('Elapsed time for OCR-ing this book: {time_ocr}. \nElapsed time for whole proccess: {total_time}'.format(time_ocr=elapsed_ocr, total_time=total_elapsed))
