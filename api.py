from fastapi import FastAPI
import os
from paddleocr import PaddleOCR, draw_ocr
import openai
import json
import fitz
import shutil
import boto3

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Converting the dictionary to a dataframe
import pandas as pd

# To eliminate KMP Kernel Error
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

ocr = PaddleOCR(use_angle_cls=True, lang='en')
# img = "./page-0.jpg"
openai.api_key = "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"

# To control the randomness and creativity of the generated text by an LLM, use temperature = 0.0
chat = ChatOpenAI(temperature=0.0, openai_api_key=openai.api_key)

extraction_template = """
The following text are obtained from an output of top performing OCR model, from a structured or unstructured document in sequential order.
Perform information extraction by understanding certain key information and try to fetch its values (If the values are unknown, fill them as "None")

Format the output in JSON structure and convert all the keys to camel-casing:

text: {text}
"""

"""
1. invoiceNo
2. invoiceDate
3. invoiceTitle
4. gstin
5. itemDetails
4. totalAmount
5. gstAmount
6. grandTotal
7. shipToDetails
8. billToDetails
"""

app = FastAPI()

@app.get("/")
def home():
    return {"status": "200",
            "message":"Welcome!"}


@app.post("/pdf")
def upload(pdf):
    pdffolder = 'pdfFolder'

    os.makedirs(f'/{str(pdffolder)}', exist_ok=True) 

    # Creating an S3 access object
    obj = boto3.client("s3")
    # Downloading a csv file 
    # from S3 bucket to local folder
    obj.download_file(
        Filename=f'/{str(pdffolder)}/{str(pdf)}',
        Bucket="invoice-pdfs-v01",
        Key=pdf
    )

    # Create a document object

    doc = fitz.open(f'/{str(pdffolder)}/{str(pdf)}')  # or fitz.Document(filename)

    pdf= pdf.split('.')

    os.makedirs(f'imgFolder/{pdf[0]}', exist_ok=True) 

    # Render and save all the pages as images
    
    for i in range(doc.page_count):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        pix.save(f"imgFolder/{pdf[0]}/page-%i.png" % page.number)
    
    st = ""
    j = 0
    for images in os.listdir(f"imgFolder/{pdf[0]}"):
        j+=1
        # check if the image ends with png
        if (images.endswith(".png")):

            result = ocr.ocr(f'imgFolder/{pdf[0]}/'+images, cls=True)


            # Empty Dictionary
            output_dict = dict()
            # Iterating through the results from Paddle OCR
            for idx in range(len(result)):
                i=0
                res = result[idx]
                for line in res:
                    # Unpacking each line
                    bbox = line[0]
                    preds, score = line[1]
                    # Adding each new dictionary with an iterator key
                    output_dict[i] = {'Bbox':bbox, 'Score':score, 'Text':preds}
                    i+=1

            # Transposing the df so we get all the records respective to the iterator key
            result_df = pd.DataFrame(output_dict).T
            result_string = result_df["Text"].to_list()
            st += 'Page - {a} \n'.format(a=j)
            st += ' '.join(str(x) for x in result_string)
            st += '\n'

    prompt_template = ChatPromptTemplate.from_template(extraction_template)

    messages = prompt_template.format_messages(text=st)
    response = chat(messages)

    res = json.loads(response.content)

    # Delete a directory
    shutil.rmtree("imgFolder")   

    return res