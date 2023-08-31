import cv2
import numpy as np
from docx import Document
import fitz
import face_recognition
from skimage.io import imread
# from id_validator import process_document
from google.api_core.exceptions import InvalidArgument
from skimage.transform import resize
import logging
import pymongo
import sys

###DB Connection###

try:
  client = pymongo.MongoClient("mongodb+srv://dban3019:Dellaware%401101@sandbox.cry0dck.mongodb.net/?retryWrites=true&w=majority")
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

db = client.Resume_Scanner

my_collection = db["Resume_Scanner_Collection"]
#function to input resume in pdf format and id in jpeg format and upload in Resume_Scanner mongodb database
def insert():
    print('Enter your ID document')  
    id=input()
    print('\n\tPlease enter the path where your file is stored:')
    path=input()
    print("\n")
    try:
        with open(path, 'rb')as f:
            my_file=(f).read()
            #print(type(my_file))
            my_collection.insert({'id':id,'resume':my_file})
    except FileNotFoundError :
            print ("File not found.")
            else:
                                       print ('Document uploaded successfully.')
       except Exception as e:
           print (e.__doc__)
       finally:
           pass      
       def get_data ():
           for i in range(len(my_collection)):
           data=[]
       for x in my_collection['resume']:
           data.append((x))
       return data
       def deleteData () :
           my_collection.delete_one({"id":id})
       def updateData () :
           my_collection.update_one({ "id" : id }, { "$set":{ "name":"<NAME>" } })
       def searchData () :
           query={"id":{"$eq":id}}
       result=get_data()
       print(result[0])
       while True:
           choice=int(input('''What do you wish to do? \n1-Upload new Document.\n2-Delete existing Document.\


    





# Configure the logging settings
logging.basicConfig(level=logging.DEBUG,  # Set the minimum logging level
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Define the log message format

# Create a logger instance
logger = logging.getLogger()

# Create a console handler and set its log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set the desired log level for console logs

# Create a formatter and add it to the console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)



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
    logger.info("rotates "+ str(len(rotates)))
    for rt_img in rotates:
        # Detect faces in the image
        logger.info("fetching face ...")
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


def is_fake(cv_path, id_path, cvimages, idimages, cv_data, id_data):
    # Initializations
    (overallStat, matchtype) = ('FAIL', 'NO-Match')

    (passed_criterias, failed_criterias, analysed_data_id,
     analysed_data_cv) = (None, None, None, None)

    # extract face from CV
    logger.info("getting Images")
    face_from_cv = extract_human_faces(cv_path, cvimages)
    logger.info("CV images fetched")
    faces_from_id = extract_human_faces(id_path, idimages,True)
    logger.info("id Images fetched")
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
    logger.info("comparing images")
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
    return {
        'CV_MATCH': matchtype,
        'ID-Authentication':None,
        'Id-Summary': None,
        'Over-All-Status': overallStat}
        
    