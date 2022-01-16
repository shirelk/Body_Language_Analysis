from datetime import datetime
from tkinter import *
import cv2
from PIL import Image
from guizero import *
from POSE_DETECTION.pose_classifer import PoseClassifier
import recommendation as r

'''
#TODO
pip3 install guizero
pip3 install guizero[images]
set READTHEDOCS=True
pip install picamera
'''

DATA_PATH = 'POSE_DETECTION/images'
POSITIVE_EMO = ['positive_interaction', 'authoritative', 'appriciation', 'confidence', 'calm', 'excitement', 'happines',
                'reliability']
NEGATIVE_EMO = ['insecure', 'fear', 'discomfort', 'anger', 'shyness', 'confusion', 'stubbornness',
                'interest in surroundings']


# Functions------------------------------------------------
def classify_pose(path):
    pose_classifier = PoseClassifier(r'..\POSE_DETECTION\model')
    poses = pose_classifier.classify_pose(path)
    return poses


def get_new_name():
    n_file = open('new_images/number', 'r+')
    number = n_file.read()
    n_file.seek(0)
    n_file.truncate()
    n_file.write(str(int(number) + 1))
    n_file.close()
    curr_time = datetime.today().strftime("%d-%m-%Y--%H%M%S")
    return 'new_images/' + 'img' + number + '_' + curr_time + '.jpg'


def view_img(img_path):
    poses = classify_pose(img_path)
    visual(poses, POSITIVE_EMO, NEGATIVE_EMO)


def upload_img():
    filename = browseFiles()
    im = Image.open(filename)
    if im.format != 'jpg':
        im = im.convert("RGB")
    if im.width > im.height and (im.width > 960 or im.height >960 ):
        im = im.rotate(90)
    filename = get_new_name()
    viewer.image = im
    im.save(filename)
    view_img(filename)


def capture_img():
    cam = cv2.VideoCapture(0)
    frame = cam.read()[1]
    filename = get_new_name()
    cv2.imwrite(filename, frame)
    im = Image.open(filename)
    viewer.image = im
    view_img(filename)


def recommand(*emo):
    rec = Window(app, title='Analysis', width=740, height=700)
    rec.bg = 'beige'
    rec.font = 'Calibri'
    rec._text_size = 15
    txt_rec = Text(rec, align='center')
    txt_rec.value = r.rec[''.join(emo)]
    txt_rec.align = 'left'
    rec.show()


def visual(emo_res, pos, neg):
    button_list = {}
    pos_box = Box(app, grid=[1, 0, 1, 2], align='left')
    neg_box = Box(app, grid=[2, 0, 1, 2], align='left')
    for emo in pos:
        im = Image.open('emotion_icons/' + emo + '.jpg')
        im = im.resize((50, 50))
        box = Box(pos_box, align='top')
        PushButton(box, command=recommand, args=emo, align='right', image=im)
        Emo = emo[0].upper() + emo[1:]
        Text(box, align='right', text=Emo, height=4, width=21)
        button_list[emo] = box
        if emo_res is not None and emo in emo_res:
            button_list[emo].bg = 'LightCyan2'
        else:
            button_list[emo].bg = 'ivory2'
    for emo in neg:
        im = Image.open('emotion_icons/' + emo + '.jpg')
        im = im.resize((50, 50))
        box = Box(neg_box, align='top')
        PushButton(box, command=recommand, args=emo, align='right', image=im)
        Emo = emo[0].upper() + emo[1:]
        Text(box, align='right', text=Emo, height=4, width=21)
        button_list[emo] = box
        if emo_res is not None and emo in emo_res:
            button_list[emo].bg = 'LightCyan2'
        else:
            button_list[emo].bg = 'ivory2'


# Function for opening the file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/Pictures",
                                          title="Select a File",
                                          filetypes=(("IMAGE_FILES",
                                                      "*.jpg*"),
                                                     ("all files",
                                                      "*.*")))

    return filename


# APP-----------------------------------------------------
NAME = 'AI_PROJECT'
MESSAGE = 'Please insert image'
BG_IMAGE = 'emotion_icons/mad.jpg'
app = App(title=NAME, layout='grid', height=732, width=985)
app.bg = 'pink1'
app.font = 'Calibri'
# APP Widgets---------------------------------------------------
b = Box(app, grid=[0, 1])

up = PushButton(b, command=upload_img, text='Upload', align='left', height=5, width=30)
up.bg = 'pink1'

take = PushButton(b, command=capture_img, text='Take a picture', align='left', height=5, width=30)
take.bg = 'pink1'

viewer = Picture(app, image=BG_IMAGE, grid=[0, 0], height=500, width=480)
view_img(BG_IMAGE)

Text(app, grid=[0, 2, 3, 1], height=4, width=120, bg='pink1', align='top',
     text='For an explanation of image analysis and additional recommendations for a specific classification:\n Click '
          'the icon button next to the classification.')

# Display---------------------------------------------------
app.display()
