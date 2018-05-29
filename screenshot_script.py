import time
from selenium import webdriver
import os

#path to index.html on your local machine
url = "file://C:\Program Files\IPOS\Data\Files\index.html"

#set path to the dynamic.js file on your machine
pathToJSfile = "C:\Program Files\IPOS\Data\Files\dynamic.js"

#list of locales for QA
locales = ['ru','fr'] #en-us html is different than other locales, so exclude it during the testing

def replace_locale_in_dynamicJS(locale, pathToJSfile):

    with open(pathToJSfile,'r') as file:
        data = file.readlines()

    #iterating every line to find the right line, as possibly the file might change later
    for i in data:
        if '"locale":' in i:
            index = data.index(i)
            data[index] = '  "locale": "' + locale + '",\n'

    new_file = open(pathToJSfile, 'w')
    for line in data:
        new_file.write("{}".format(line))

#creating folders for screenshots for each locale, if not present in the directory where script is locacted
cwd = os.getcwd()
if not os.path.exists(cwd+'\screenshots'):
    os.makedirs(cwd+'\screenshots')

for locale in locales:
    if not os.path.exists(cwd+'\screenshots\\'+locale):
        os.makedirs(cwd+'\screenshots\\'+locale)


#check resolution
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

######
if __name__ == "__main__":

    #checking the resolution
    # if screensize != (1366, 768):
    #     print('CHANGE THE RESOLUTION!!!', screensize)
    # else:
        print('Running with', screensize) # create time variable and break/continue
        for locale in locales:
            #create a function for everthing in while with a timeout
            while True:
                try:
                    replace_locale_in_dynamicJS(locale, pathToJSfile)

                    driver = webdriver.Ie()
                    driver.get(url)

                    batteryButton = driver.find_element_by_xpath('//*[@id="nav_battery"]/div[1]')
                    batteryButton.click()
                    driver.save_screenshot('screenshots/' + locale + '/battery.png')


                    #in portrait mode there is scrolling button that has to be clicked to get to the needed item in the navigation bar
                    try:
                        scrollbutton = driver.find_element_by_xpath('// *[ @ id = "feature-nav"] / div[3]')
                        scrollbutton.click()
                        #break
                    except Exception as e:
                        print('{}'.format(str(e)))


                    graphicsButton = driver.find_element_by_xpath('//*[@id="nav_graphics"]')
                    graphicsButton.click()
                    driver.save_screenshot('screenshots/' + locale + '/graphics.png')

                    aboutGraphics = driver.find_element_by_xpath(
                        '// *[ @ id = "stage_graphics"] / div / button [1] / div')
                    aboutGraphics.click()
                    driver.save_screenshot('screenshots/' + locale + '/aboutGraphics.png')

                    closeAboutGraphics = driver.find_element_by_xpath(
                        '//*[@id="stage_graphics"]/stage-article-overlay/div/div[1]')
                    driver.quit()

                    print('Done: ', locale)
                except:
                    print('Something went wrong for', locale)
                    continue
                break
        print('All is done')

########
