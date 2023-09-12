# from ultralytics import YOLO
# import cv2
# import math 
# import streamlit as st
# import os


# col_project_name, col_img  = st.columns([3, 1])
# col_img.image("util/imgs/logo.png")
# col_project_name.header("Deteccao de Coca ou Fanta")
# st.markdown("---", unsafe_allow_html = True)

# st.info("Para iniciar a deteccao de objetos, por favor selecione a checkbox: 'Run'")

# run = st.checkbox("Run")
# FRAME_WINDOW = st.image([])
# cap = cv2.VideoCapture(1)
# TH_CONFIDENCE = 0.1

# model = YOLO("model/model.pt")
# # model = YOLO("/home/henrico/Github/SAP-GPT/model/model.pt")

# classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
#               "traffic light", "fire hydrant", "stop sign", "parkpiping meter", "bench", "bird", "cat",
#               "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
#               "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
#               "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
#               "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
#               "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
#               "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
#               "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
#               "teddy bear", "hair drier", "toothbrush", "glasses", "wallet",
#               ]


# # with open("yolo_cfg/yolov3.txt", "r") as file:  
# #     classNames = file.readlines()



# while run:
#     success, img = cap.read()
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = model(img, stream=True)

#     for r in results:
#         boxes = r.boxes

#         for box in boxes:
#             confidence = math.ceil((box.conf[0]*100))/100

#             if (confidence > TH_CONFIDENCE):

#                 x1, y1, x2, y2 = box.xyxy[0]
#                 x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

#                 cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

#                 cls = int(box.cls[0])
#                 print("Class name -->", classNames[cls])
#                 os.system("clear")
#                 if classNames[cls] == "bottle":
#                     org = [x1, y1]
#                     font = cv2.FONT_HERSHEY_SIMPLEX
#                     fontScale = 1
#                     color = (255, 0, 0)
#                     thickness = 2
#                     org_conf = [x2, y2]

#                     cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
#                     cv2.putText(img, f"{confidence}", org_conf, font, fontScale, color, thickness)

#     FRAME_WINDOW.image(img)



from ultralytics import YOLO
import cv2
import math 
import streamlit as st
import os
import tensorflow as tf
from PIL import Image
import numpy as np
from keras.applications.vgg16 import preprocess_input
from src.functions import *
import pandas as pd
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(initial_sidebar_state = "collapsed",
                   page_icon = "util/imgs/logo-horus.png",
                   page_title = "NoName")

st.markdown(
    """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """,
    unsafe_allow_html = True)

st.image("./util/imgs/logo-horus.png", width = 200)


col_project_name, col_img, button_back  = st.columns([3, 1, 1])
col_img.image("util/imgs/logo.png")
col_project_name.header("Detecção de Coca ou Fanta")
st.markdown("---", unsafe_allow_html = True)

if button_back.button("Voltar para Tela Inicial"):
    switch_page("main")


st.info("Para iniciar a detecção de objetos, por favor selecione o metodo de detecção de Objetos: Foto ou Video")

f_v = st.selectbox(options = ["Selecione", "Foto", "Video"], label = "Método de Detecção")

new_model = tf.keras.models.load_model('model/model/model-refri.h5')

TH_CONFIDENCE = 0.1

if f_v == "Video":
    run = st.checkbox("Run")
    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(0)
    

    while run:
        success, img = cap.read()
        img_to_predict = Image.fromarray(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        validation_batch = np.stack([preprocess_input(np.array(img_to_predict.resize((224,224))))])
        preds = new_model.predict(validation_batch)

        coca_conf = preds[0,0] * 100
        fanta_conf = preds[0,1] * 100

        print("{:.0f}% Coca, {:.0f}% Fanta".format(coca_conf, fanta_conf))

        label = "{:.0f}% Coca, {:.0f}% Fanta".format(coca_conf, fanta_conf)
        img = cv2.putText(img, label, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)


        FRAME_WINDOW.image(img)

elif f_v == "Foto":

    pic_or_send = st.radio(options = ["Tirar foto", "Enviar foto"], label = "Selecione")

    if pic_or_send == "Tirar foto":
        img_file_buffer = st.camera_input("Tirar uma foto")
        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            img_to_predict = Image.fromarray(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            validation_batch = np.stack([preprocess_input(np.array(img_to_predict.resize((224,224))))])
            preds = new_model.predict(validation_batch)

            coca_conf = preds[0,0] * 100
            fanta_conf = preds[0,1] * 100

            if coca_conf > fanta_conf:
                st.success("{:.0f}% Coca, {:.0f}% Fanta".format(coca_conf, fanta_conf))
            else:
                st.success("{:.0f}% Coca, {:.0f}% Fanta".format(coca_conf, fanta_conf))

    elif pic_or_send == "Enviar foto":
        img_file_buffer = st.file_uploader("Escolher uma imagem do seu PC", accept_multiple_files = False)
        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            img_to_predict = Image.fromarray(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            validation_batch = np.stack([preprocess_input(np.array(img_to_predict.resize((224,224))))])
            preds = new_model.predict(validation_batch)

            coca_conf = preds[0,0] * 100
            fanta_conf = preds[0,1] * 100

            st.image(img, width = 400)

            if coca_conf > fanta_conf:
                st.success("{:.0f}% Coca, {:.0f}% Fanta".format(coca_conf, fanta_conf))
            else:
                st.success("{:.0f}% Coca, {:.0f}% Fanta".format(coca_conf, fanta_conf))

id = st.text_input("Digite o ID do Dataframe: ")

if ("coca_conf" in globals()) and ("fanta_conf" in globals()):
    st.header("Previsão realizada e inserida na base de dados!")
    if coca_conf > fanta_conf:
        dicionario_gpt = return_produtos_df("Refrigerante Coca Cola")
        df = pd.DataFrame(dicionario_gpt, index = [len(dicionario_gpt)])
        df['Descrição'] = df['Descrição'].str.replace('\n\n', '')
        st.dataframe(df, use_container_width = True)
        teste = ler_dataframe_e_converter(df)
        append_gpt_to_df_all(consultar_email_em_log(), teste[1], id)
        
    else:
        dicionario_gpt = return_produtos_df("Refrigerante Fanta Laranja")
        df = pd.DataFrame(dicionario_gpt, index = [len(dicionario_gpt)])
        df['Descrição'] = df['Descrição'].str.replace('\n\n', '')
        st.dataframe(df, use_container_width = True)
        teste = ler_dataframe_e_converter(df)
        append_gpt_to_df_all(consultar_email_em_log(), teste[1], id)
        
else:
    st.warning("Prediçao ainda não realizada")