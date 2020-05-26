from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from time import sleep
import os, shutil, re
from fpdf import FPDF
from PIL import Image


#class for returning url and book_title
class pre_checks():
    def read_link(self, book_url):
        read_url = book_url
        book_title = book_url.split(r'/')[-1]
        return read_url, book_title

#class for most of the action
class Screenshots:
    dirpath = os.getcwd()       #find script's root

    #function for doing log in
    def login(self,email,password, sign_mail, sign_buttom):
        if sign_mail == None:
            sign_mail = '/html/body/div[2]/div/div/div/div/div/div[1]/div[2]/div[2]/a'
        if sign_buttom == None:
            sign_buttom = '/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/form/fieldset/div[3]/button'
            print("none")
        try:            #typing email and password and then clicking to Log In
            self.driver.find_element_by_id('login_or_email').send_keys(email)
            self.driver.find_element_by_id('login_password').send_keys(password)
            sign_buttom = '/html/body/div[4]/div[2]/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/form/fieldset/div[3]/button'
            self.driver.find_element_by_xpath(sign_buttom).click()
            print("Clicked Log In buttom")
                                                   
        except NoSuchElementException:
            self.driver.quit()
            print('NoSuchElementException on login() function; lines 24-39')
        
    #Checks if its in Portuguese version of the site and if not, make the change    
    def check_language(self):
        language = self.driver.find_element_by_xpath('/html/body/span[1]/div/header/div[1]/div[4]/div[1]/div/div/a/span[2]').text
        if language != 'PT':
            print('Setting language to Portuguese')
            self.driver.find_element_by_xpath('/html/body/span[1]/div/header/div[1]/div[4]/div[1]/div/div/a/span[3]').click()
            self.driver.find_element_by_xpath('/html/body/span[1]/div/header/div[1]/div[4]/div[1]/div/div/div/div[2]/ul/li[3]/a/div').click()
        else:
            print('Right site language!')

    #checks if its logged or not and if not, log in
    def login_check(self, email, password):
        try:
            arrow = self.driver.find_element_by_xpath('/html/body/span[1]/div/header/div[1]/div[4]/div[2]/a/div/span')
            logged_check = True
        except:
            logged_check = False
        if logged_check == False:
            #Start to log in
            self.driver.find_element_by_xpath('/html/body/span[1]/div/header/div[1]/div[4]/div[2]/div/a[2]').click()
            print("First click to log in done!")
            sleep(3)
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/a').click()
            print("Second click to log in done!")

            sign_mail_read = '/html/body/div[3]/div[2]/div/div[3]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/a'
            sign_buttom_read = '/html/body/div[4]/div[2]/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/form/fieldset/div[3]/button'
        
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/a').click()
            print("Third click to log in done!")
            sleep(3)
            self.login(email,password, sign_mail_read, sign_buttom_read)    #Execute login
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/fieldset/div[3]/button').click()
            print("Login sucessfull")
            sleep(7)
            self.driver.back()
            print("Got back to books page")
            sleep(5)
        else:
            print("Already loged!")         #If already loged will continue

    #checks percentage and goes back to 0% if is not already
    def check_percentageIsZero(self):
        #read actual percentage, page(pagina) and final book page (paginafinal) Sorry for not translating the objects name
        percentage_read = int(self.driver.find_element_by_class_name('percentage_read').text.replace(r'% lido',''))
        pagina = int((self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/span/div/nav/div[2]/div[2]/div').text.replace("PÁGINA", '')).split(" DE ")[0])
        paginafinal = int((self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/span/div/nav/div[2]/div[2]/div').text.replace("PÁGINA", '')).split(" DE ")[1])
        print("%: ",percentage_read,". pag: ", pagina) #prints the status of the reading
        #goes back to 0% or 1st page
        while percentage_read != 0 or pagina != 1:
            try:
                self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/span/div/nav/div[2]/div[2]/a[1]/span[2]').click()
                percentage_read = int(self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/span/div/nav/div[2]/div[3]').text.replace(r'% lido',''))
                pagina = int(self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/span/div/nav/div[2]/div[2]/div').text.replace("PÁGINA", '').split(" DE ")[0])
                if pagina == 1:
                    return [percentage_read, pagina, paginafinal]
            except:
                print("Error within percentage if its not 0%. Lines 83-99")
                break
        return [percentage_read, pagina, paginafinal]

    def remove_bookmark_line(self):                 #removes bookmark line from the superior right corner with a js script
        bookmark = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/span[2]')
        element_id = bookmark.get_attribute("id")
        js_string = str("var element = document.getElementById(\""+element_id+"\");element.remove();")
        self.driver.execute_script(js_string)

    #function to try to click the 'save book' popup so it doesn't appers in the screenshot
    def popup_click(self):
        popup_click = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div[1]/span/div/div/a[1]/span[1]') #opinion popup
        try:
            popup_click.click()
            print("Saving popup dismissed!")
        except NoSuchElementException:
            print("Didnt saving popup! Great!")
            pass
        except ElementNotInteractableException:
            print('Didnt found save book popup! Great!')
            pass
    
    def update_percentage(self):        #function to update the percentage and page progress
        percentage_read = int(self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/span/div/nav/div[2]/div[3]').text.replace(r'% lido',''))
        pagina = int(self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/span/div/nav/div[2]/div[2]/div').text.replace("PÁGINA", '').split(" DE ")[0])
        return percentage_read, pagina
    #########################################################################################
    def screenshot(self, read_url, book_title, email, password, book_id):
        img_path = os.path.join(self.dirpath,book_id, '')
        #set chromedriver options and load it
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=selenium") 
        chrome_options.add_argument("--start-fullscreen")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver,100)
        options = {
            'page-width' : '211',
            'page-height': '298',
            'enable-local-file-access':''
        }
    
        #go to book url
        self.driver.get(read_url)
        sleep(5)
        self.check_language() #check if its in Portugues and if not, change
        self.login_check(email,password)    #Check if its logged and if not, login

        #click the 'read this book now' buttom
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[3]/div/div/section/div/div/section/a').click()
        print("Read page done")
        sleep(7)
        percentage_read, pagina, paginafinal = self.check_percentageIsZero()    #checks the percentage read and if != 0
        try:                                                                    #goes back to the start of the book
            sleep(2)
            print("Start screenshot proccess")
            
            self.remove_bookmark_line()         #removes bookmark line from the superior right corner

            columns_1 = []
            columns_2 = []
            i = 1
            while percentage_read != 100 or pagina != paginafinal:
                sleep(2)
                
                self.popup_click()  #every page trying to click the 'save book' popup. Still get problems some time

                sleep(1)
                file_name1 = str(book_title)+'_'+str(i).zfill(len(str(paginafinal)))  #filename for first colum/page
                #first column/page screenshot
                col1 = self.driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div/div[2]/div[1]/div[2]/div[1]").screenshot(img_path+file_name1+'_1.png')
                try:
                    file_name2 = str(book_title)+'_'+str(i).zfill(len(str(paginafinal)))  #filename for second colum/page
                    #second column/page screenshot
                    col2 = self.driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div/div[2]/div[1]/div[2]/div[2]").screenshot(img_path+file_name2+'_2.png')
                except Exception as e:
                    print(e)
                    print("Column 2 not found in this page") #Some books only shows one column per time
                    pass
                #Pass to next page clicking the right arrow
                self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div[1]/div[1]/button[2]').click()
                print("Next page")
                percentage_read, pagina = self.update_percentage()   #update percentage and page progress
                print("%", percentage_read, ". Page= ", i)
                i +=1       #Adds to i counter
            if percentage_read == 100:
                #when completed closes chrome window
                self.driver.quit()

        except NoSuchElementException:
            self.driver.quit()
            print('NoSuchElementException in screenshot function from lines 150-189')


    ##################################################################################

#class for generating pdf file from screenshots
class PDF_Gen(FPDF):
    dirpath = os.getcwd()       #find script's root
    #
    #Addapted PHP code from https://gist.github.com/benshimmin/4088493. 
    #Scale to fit and centre-align images
    #I teaked to A4 @ 300 dpi - 3507x2480 pix
    DPI = 300
    MM_IN_INCH = 25.4
    A4_HEIGHT = 210
    A4_WIDTH = 297
    #tweak these values (in pixels)
    MAX_WIDTH = 3507
    MAX_HEIGHT = 2480

    def pixelsToMM(self,val):   #funct to convert pixels to mm
        val = (val*self.MM_IN_INCH)/self.DPI
        return val

    def footer(self):               #sets pages footers with page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 9)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')

    def get_imgs_path(self,lista, img_path):    #returns the list of image_files in book _id directory
        for file in os.listdir(img_path):
            if file.endswith(".png"):
                lista.append(file)
        return lista
    
    def resizeToFit(self,imgFilename):      #funct to return 'new' image sizes for centralization
        im = Image.open(imgFilename)
        sizes = list(im.size)
        width = sizes[0]
        height = sizes[1]

        widthScale = self.MAX_WIDTH / width
        heightScale = self.MAX_HEIGHT / height

        scale = min(widthScale, heightScale)

        return [round(self.pixelsToMM(scale * width)),round(self.pixelsToMM(scale * height))]

    def centreImage(self,img_file):     #function to centralize images in pdf page
        newsizes = list(self.resizeToFit(img_file))
        width = newsizes[0]
        height = newsizes[1]
        #sets image withing right coordenates
        self.pdf.image(img_file, (self.A4_HEIGHT - width) / 2,(self.A4_WIDTH - height) / 2,width,height)

    def img_to_pdf(self,book_title, book_id):       #creates the pdf
        lista = []
        img_path = os.path.join(self.dirpath, book_id, "")
        lista = self.get_imgs_path(lista, img_path) #get the list of imgs in book_id directory

        if len(lista) != 0:
            self.pdf = FPDF()
            for i in range(len(lista)): #FPDF options
                print("Writing page nº: {page} of {total}".format(page= i+1, total= len(lista)))
                self.pdf.set_font('Times', '', 12)
                self.pdf.add_page('P')
                self.centreImage(str(os.path.join(img_path,lista[i])))
                self.pdf.alias_nb_pages()
            print("Saving file, please wait. It can take some time if it is a big book!")
            self.pdf.output(book_title + '_IMG.pdf', 'F')       #saves pdf_IMG file
            print("PDF '{book_title}' saved in script's root!".format(book_title='{title}(...)'.format(title=book_title[:20])))
        print("Deleting %i temporary image page files from root."% (len(lista)+1))
        shutil.rmtree(img_path)     #delestes book_id directory


    def main(self,book_title, book_id):
        self.img_to_pdf(book_title, book_id)