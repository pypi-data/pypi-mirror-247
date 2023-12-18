import cv2
import easyocr
import json
import threading
import logging

language_need_to_extract= ['en']
reader = easyocr.Reader(language_need_to_extract)
drawing = False
start_x, start_y, end_x, end_y = -1, -1, -1, -1
#new_width = 725
#new_height = 1025
# Configure the logging module
logging.basicConfig(filename='Result.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.basicConfig(filename='Error.log', level=logging.exception, format='%(asctime)s - %(levelname)s - %(message)s')
#####################################################################
def ocr_scan(img)->json:
    try:
        result = reader.readtext(img,detail=0)
        result_json = json.dumps(result,indent=4)
        logging.info(result_json)
        #return result_json 
    except Exception as e:
        result=f'Failed to process due to {e}'
        logging.exception(result)


        
       

def draw_roi(event, x, y, flags, param) ->json:
    
    global start_x, start_y, end_x, end_y, drawing
    img = param
    try:
        if event == cv2.EVENT_LBUTTONDOWN:
            # User pressed the left mouse button, start drawing
            start_x, start_y = x, y
            drawing = True
        elif event == cv2.EVENT_LBUTTONUP:
            # User released the left mouse button, stop drawing and define the ROI
            end_x, end_y = x, y
            drawing = False

            # Draw the rectangle on the original image
            cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 255), 2)
            cropped_img = img[start_y:end_y, start_x:end_x]
            result = reader.readtext(cropped_img, detail=0)
            result_json = json.dumps(result,indent=4)
            logging.info(result_json)
            return print(result_json)
    except Exception as e:
        result=f'Failed to process due to {e}'
        logging.exception(result)

def mouse_boundary(img):
    try:
        cv2.namedWindow("image")
        cv2.setMouseCallback("image",draw_roi,img)
        # Main loop
        while True:
            cv2.imshow("image", img)
            if cv2.waitKey(1) == 27:
                break
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
    except cv2.error as e:
        result=f'Failed to process due to {e}'
        logging.exception(result)

        
##########################################################################

# Create two threads
def Teaxt_extraction_oparation(img):
    thread1 = threading.Thread(target=ocr_scan, args=(img,))
    thread1.start()
    thread1.join()
    thread2 = threading.Thread(target=mouse_boundary,args=(img,))
    thread2.start()
    thread2.join()

def full_process(func):
    def wrapper(*args, **kwargs):
        status=f'Pro funtanality of AROOCR'
        img=func(*args, **kwargs)
        Teaxt_extraction_oparation(img)
        logging.info(status)
    return wrapper


def only_text_extraction(func):
    def wrapper(*args, **kwargs):
        status=f'Basic funtanality of AROOCR'
        img=func(*args, **kwargs)
        ocr_scan(img)
        logging.info(status)
    return wrapper


def hilited_text_extraction(func):
    def wrapper(*args, **kwargs):
        status=f'Pro funtanality of AROOCR'
        img=func(*args, **kwargs)
        mouse_boundary(img)
        logging.info(status)
    return wrapper

@full_process
def image_path(path):
        image_path=str(path)
        img=cv2.imread(image_path)
        return img


@only_text_extraction
def image_path_full(path):
    image_path=str(path)
    img=cv2.imread(image_path)
    return img

@hilited_text_extraction
def extracted_image(path):
    global new_width, new_height
    image_path=str(path)
    img=cv2.imread(image_path)
    height, width, _ = img.shape

    while True:
        if height == new_height and width == new_width:
            return img
        else:
            height = new_height
            width = new_width
            break

    resized_image = cv2.resize(img, (new_width, new_height))
    return img
    


