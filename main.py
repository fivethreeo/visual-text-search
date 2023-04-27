import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
import PIL.Image as Image
import pytesseract
from pytesseract import Output
# specify the path to the webdriver executable
debug = True
#debug = False

def photoshop_brightness(input_img, brightness = 0):
    ''' input_image:  color or grayscale image
        brightness:  -127 (all black) to +127 (all white)

            returns image of same type as input_image but with
            brightness adjusted

    '''
    img = input_img.copy()
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        cv2.convertScaleAbs(input_img, img, alpha_b, gamma_b)

    return img
scale = 1.2
options = Options()
if not debug:
    options.add_argument('-headless')
profile = webdriver.FirefoxProfile()
profile.set_preference("layout.css.devPixelsPerPx", "%f" % scale)
driver = webdriver.Firefox(options=options, firefox_profile=profile)

# navigate to the webpage
driver.get('https://www.myfxbook.com/community/outlook')
driver.implicitly_wait(10) # seconds
time.sleep(10)

# wait for page to load
original_size = driver.get_window_size()
required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(required_width, required_height)
time.sleep(2)

driver.execute_script('var el = document.createElement("div"); el.style.height="200px"; el.style.width="100px"; el.style.background="red"; el.style.zIndex=20000; el.style.left="0px"; el.style.top="0px";  el.style.position="absolute"; document.body.appendChild(el);')

screenshot = driver.get_screenshot_as_png()


img = Image.open(io.BytesIO(screenshot))
if debug:
    img.show()
# Convert the image to grayscale
dark = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGR)
dark = photoshop_brightness(dark, -120)
gray = cv2.cvtColor(dark, cv2.COLOR_BGR2GRAY)

# Apply thresholding to the image
# thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Get the character boxes using pytesseract

d = pytesseract.image_to_data(dark, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    if d['text'][i].strip() == "Continue":
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        print(d['text'][i])

        pos = ((x+4)/scale,(y+4)/scale)
        addel = """
        el = document.createElement('div');
        el.style.height='10px';
        el.style.width='10px';
        el.style.background='red';
        el.style.zIndex=20000;
        el.style.left='%ipx'; el.style.top='%ipx';
        el.style.position='absolute';
        document.body.appendChild(el);
        """ % pos
        # driver.execute_script(addel)
        click = """
        el = document.elementFromPoint(%i, %i);
        el.click();
        return el.innerHTML
        """ % pos
        print(click)
        print(driver.execute_script(click))
        cv2.rectangle(dark, (x, y), (x + w, y + h), (0, 255, 0), 2)

if debug:
        
    screenshot = driver.get_screenshot_as_png()

    img = Image.open(io.BytesIO(screenshot))
    img.show()

    Image.fromarray(dark).show()
"""

time.sleep(2)
# wait for page to load
original_size = driver.get_window_size()
required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(required_width, required_height)
# driver.save_screenshot(path)  # has scrollbar
# driver.find_element_by_tag_name('body').screenshot(path)  # avoids scrollbar
time.sleep(2)

screenshot = driver.get_screenshot_as_png()
# driver.set_window_size(original_size['width'], original_size['height'])

img = Image.open(io.BytesIO(screenshot))
img.show()

cv2img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
d = pytesseract.image_to_data(cv2img, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    cv2.rectangle(cv2img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(d['text'][i])
# Display the image with character boxes
Image.fromarray(cv2img).show()
 """