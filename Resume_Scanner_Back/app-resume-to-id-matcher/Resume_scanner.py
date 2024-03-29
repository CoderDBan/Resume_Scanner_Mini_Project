import cv2
import numpy as np
from docx import Document
import fitz
import face_recognition
from skimage.io import imread
import pymongo
import sys
import logging as log
log.basicConfig(level=log.INFO)
###DB Connection###

try:
  client = pymongo.MongoClient("mongodb+srv://dban3019:Dellaware%401101@sandbox.cry0dck.mongodb.net/?retryWrites=true&w=majority")
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

db = client.Resume_Scanner

my_collection = db["Resume_Scanner_Collection"]
'''
Assume that the app.py file will be utilising a method from this file. the method is expected to take a file as parameter and place it in the database mentioned above. The database is of Mongo DB. the configurations are done above.

'''
#this method must take an input that is get a single file by an Id parameter namely file Id
def get_all(id):
    return my_collection.find_one("_id")
def insertOneRecordToDatabase (record):
    try :
        rec=my_collection.insert_one(record)
        return str(rec.inserted_id)
    except Exception as e:
        print('error',e,type(e))



def rotate_image(image, angle):
    # Get image dimensions
    height, width = image.shape[:2]

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(
        (width / 2, height / 2), angle, 1.0)

    # Apply rotation to the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return rotated_image


# Function to extract images if the file is of doc type
def extract_images_docx(cv_doc):
    doc = Document(cv_doc)
    iml=[]
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            image_data = rel.target_part.blob
            nparr = np.frombuffer(image_data, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            iml.append(img_np)
    return iml

# Function to extract images if the document is of PDF format
def extract_images_pdf(cv_doc):
    iml=[]
    # Open the PDF file
    pdf = fitz.open(stream=cv_doc.file._file, filetype="pdf")
    for page in pdf:
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.h, pix.w, pix.n)
        iml.append(img)
    return iml

# Function to extract human faces from another image
def get_faces(image,rotating):
    angles = [30, 60, 90, -30, -60, -90]
    faces = []
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rotates=[rgb_image]
    if rotating:
        rotates+=[rotate_image(rgb_image, angle) for angle in angles]
    log.info("rotates "+ str(len(rotates)))
    for rt_img in rotates:
        # Detect faces in the image
        log.info("fetching face ...")
        face_locations = face_recognition.face_locations(rt_img)
        # Extract the face region
        for face_location in face_locations:
            face_encoding = face_recognition.face_encodings(
                rt_img, known_face_locations=[face_location])[0]
            faces.append(face_encoding)
    return faces

# Function to extract human face Images from PDF or word document


def extract_human_faces(inp_doc, scannedpdfImages, rotating=False):
    image_list = []
    f = True
    try:
        if inp_doc.filename.endswith('.docx'):
            image_list=extract_images_docx(inp_doc.file._file)
        elif inp_doc.filename.endswith('.pdf'):
            image_list=extract_images_pdf(inp_doc)
        else:
            image_list = [imread(inp_doc.file)]
        assert(len(image_list)>0)
    except:
        if inp_doc.filename.endswith('.pdf'):
            f=not f
            image_list = [np.array(x) for x in scannedpdfImages]
        else:
            return []
    humanImages = []
    for image in image_list:
        humanImages += get_faces(image,rotating)
    return humanImages

# Function to identify Fake CV
def is_fake(cv_path, id_path, cvimages, idimages):
    # Initializations
    (overallStat, matchtype) = ('FAIL', 'NO-Match')
    # extract face from CV
    log.info("getting Images")
    face_from_cv = extract_human_faces(cv_path, cvimages)
    log.info("CV images fetched")
    faces_from_id = extract_human_faces(id_path, idimages,True)
    log.info("id Images fetched")
    if (len(faces_from_id) < 1):
        return {
            'CV_MATCH': matchtype,
            'ID-Authentication':None,
            'Id-Summary': "PROVIDED WRONG ID DOCUMENT",
            'Over-All-Status': overallStat}
    if (len(face_from_cv) < 1):
        return {
            'CV_MATCH': matchtype+" PROVIDED CV without a picture ".capitalize(),
            'ID-Authentication':None,
            'Id-Summary': None,
            'Over-All-Status': overallStat}
    log.info("comparing images")
    for face in face_from_cv:
        matchtype = "Full Match" if sum(face_recognition.compare_faces(
            faces_from_id, face)) != 0 else "No-Match"
        if matchtype != "Full Match":
            return {
            'CV_MATCH': matchtype + " - Faces Don't match ",
            'ID-Authentication':None,
            'Id-Summary': None,
            'Over-All-Status': overallStat}            
    # un-comment theese lines and comment the others to stop the description invocation
    overallStat='PASS'
    return {
        'CV_MATCH': matchtype,
        'ID-Authentication':None,
        'Id-Summary': None,
        'Over-All-Status': overallStat}
def validate_and_update(details):
    res=is_fake(details["cv_path"],details["id_path"],details["cv_images"],details["id_images"])
    details["result"]=res
    details["cv_path"],details["id_path"],details["cv_images"],details["id_images"]=None,None,None,None
    return insertOneRecordToDatabase(details)
    
    