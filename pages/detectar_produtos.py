# import cv2
# import math 
# import streamlit as st
# import os
# import tensorflow as tf
# from PIL import Image
# import numpy as np
# from keras.applications.vgg16 import preprocess_input
# from src.functions import *
# import pandas as pd
# from streamlit_extras.switch_page_button import switch_page
# from keras.models import load_model 


# def insert_result():
#     if "results" in globals():
#         st.header("Previsão realizada e inserida no Horus!")
#         dicionario_gpt = return_produtos_df(results["class"])
#         df = get_user_dataframes()
#         novos_df = pd.DataFrame({coluna: [results["class"]],'horus': [dicionario_gpt]})
#         df = pd.concat([df, novos_df], ignore_index=True)
#         st.dataframe(df, use_container_width = True)
#         colunas, dados = ler_dataframe_e_converter(df)
#         adicionar_dataframe_para_email(colunas,dados)
#     else:
#         st.warning("Previsao nao realizada")


# st.set_page_config(initial_sidebar_state = "collapsed",
#                    page_icon = "util/imgs/logo-horus.png",
#                    page_title = "NoName")

# st.markdown(
#     """
#         <style>
#             [data-testid="collapsedControl"] {
#                 display: none
#             }
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#         </style>
#     """,
#     unsafe_allow_html = True)

# st.image("./util/imgs/logo-horus.png", width = 200)


# col_project_name, col_img, button_back  = st.columns([3, 1, 1])
# col_img.image("util/imgs/logo.png")
# col_project_name.header("Detecção de Coca ou Fanta")
# st.markdown("---", unsafe_allow_html = True)

# if button_back.button("Voltar para Tela Inicial"):
#     switch_page("main")


# st.info("Para iniciar a detecção de objetos, por favor selecione o metodo de detecção de Objetos: Foto ou Video")
# df_original = get_user_dataframes()
# df_original.drop(columns=["horus"], inplace = True)
# f_v = st.selectbox(options = ["Selecione", "Foto", "Video"], label = "Método de Detecção")
# coluna = st.selectbox("Selecione a coluna que contem os nomes dos produtos", options = df_original.columns)



# TH_CONFIDENCE = 70

# if f_v == "Video":
#     cap = cv2.VideoCapture(1)
#     frame_placeholder = st.empty()
#     start_button = st.button("Start")
#     stop_button = st.button("Stop")
    
#     if start_button:
#         while cap.isOpened() and not stop_button:
#             ret, image = cap.read()

#             if not ret:
#                 st.write("O video parou")
#                 break
 
#             results = make_predict(image)
#             img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#             if float(results["score"]) > TH_CONFIDENCE:
#                 label = results['label'].replace("_", " ")
#                 label = label.replace("?", " ")
#                 img = cv2.putText(img, label, (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

#             frame_placeholder.image(img, channels = "RGB")

#             if stop_button:
#                 break


# elif f_v == "Foto":

#     pic_or_send = st.radio(options = ["Tirar foto", "Enviar foto"], label = "Selecione")

#     if pic_or_send == "Tirar foto":
#         img_file_buffer = st.camera_input("Tirar uma foto")
#         if img_file_buffer is not None:
#             bytes_data = img_file_buffer.getvalue()
#             img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
#             img_to_predict = img
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             results = make_predict(img_to_predict)
#             st.image(img, width = 400)
#             st.success("{}".format(results["label"]))
#             insert_result()
            

#     elif pic_or_send == "Enviar foto":
#         img_file_buffer = st.file_uploader("Escolher uma imagem do seu PC", accept_multiple_files = False)
#         if img_file_buffer is not None:
#             bytes_data = img_file_buffer.getvalue()
#             img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
#             img_to_predict = img
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             results = make_predict(img_to_predict)
#             st.image(img, width = 400)
#             st.success("{}".format(results["label"]))
#             insert_result()

        
# else:
#     st.warning("Prediçao ainda não realizada")


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
from keras.models import load_model 
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration, WebRtcMode
import av
import threading
import time



st.set_page_config(initial_sidebar_state = "collapsed",
                   page_icon = "util/imgs/logotipo.png",
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
with open('css/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.image("./util/imgs/logo-horus.png", width = 200)


col_project_name, col_img, button_back  = st.columns([3, 1, 1])
col_img.image("util/imgs/logo.png")
if st.button("Voltar"):
    switch_page("main")
col_project_name.header("Detecção de Coca ou Fanta")
st.markdown("---", unsafe_allow_html = True)




st.info("Para iniciar a detecção de objetos, por favor selecione o metodo de detecção de Objetos: Foto ou Video")
df_original = get_user_dataframes()
df_original.drop(columns=["horus"], inplace = True)
f_v = st.selectbox(options = ["Selecione", "Foto", "Video"], label = "Método de Detecção")
coluna = st.selectbox("Selecione a coluna que contem os nomes dos produtos", options = df_original.columns)
TH_CONFIDENCE = 70




def insert_result_video(results, coluna_produto):
    if results.get("class", "") not in df_original[coluna_produto].to_list():
        st.header("Previsão realizada e inserida no Horus!")
        dicionario_gpt = return_produtos_df(results.get("class", ""))
        df = get_user_dataframes()
        novos_df = pd.DataFrame({coluna: [results.get("class", "")],'horus': [dicionario_gpt]})
        df = pd.concat([df, novos_df], ignore_index=True)
        st.dataframe(df, use_container_width = True)
        colunas, dados = ler_dataframe_e_converter(df)
        adicionar_dataframe_para_email(colunas,dados)
    else:
        st.warning("Produto já adicionado na base!")


def insert_result():
    if "results" in globals():
        st.header("Previsão realizada e inserida no Horus!")
        dicionario_gpt = return_produtos_df(results["class"])
        df = get_user_dataframes()
        novos_df = pd.DataFrame({coluna: [results["class"]],'horus': [dicionario_gpt]})
        df = pd.concat([df, novos_df], ignore_index=True)
        st.dataframe(df, use_container_width = True)
        colunas, dados = ler_dataframe_e_converter(df)
        adicionar_dataframe_para_email(colunas,dados)



class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.return_result_to_predict = {}


    def return_result_img(self, frame):
        results = make_predict(frame)
        return results
    

    def recv(self, frame):        
        frame_as_array = frame.to_ndarray(format="bgr24")
        results = self.return_result_img(frame_as_array)
        self.return_result_to_predict = results

        if float(results["score"]) > TH_CONFIDENCE:
            label = results['label'].replace("_", " ")
            frame_as_array = cv2.putText(frame_as_array, label, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        return av.VideoFrame.from_ndarray(frame_as_array, format="bgr24")




# Configurações do WebRTC
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]} 
)



if f_v == "Video":
    ctx = webrtc_streamer(
        key="example",
        video_processor_factory=VideoProcessor,
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"video": True, "audio": False})
    
    reset = st.empty()
    while ctx.state.playing:
        with reset.container():
            time.sleep(2)
            results = ctx.video_processor.return_result_to_predict
            # st.success(results)
            insert_result_video(results, coluna)

    
elif f_v == "Foto":

    pic_or_send = st.radio(options = ["Tirar foto", "Enviar foto"], label = "Selecione")

    if pic_or_send == "Tirar foto":
        img_file_buffer = st.camera_input("Tirar uma foto")
        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            img_to_predict = img
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = make_predict(img_to_predict)
            st.image(img, width = 400)
            st.success("{}".format(results["label"]))
            insert_result()
            

    elif pic_or_send == "Enviar foto":
        img_file_buffer = st.file_uploader("Escolher uma imagem do seu PC", accept_multiple_files = False)
        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            img_to_predict = img
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = make_predict(img_to_predict)
            st.image(img, width = 400)
            st.success("{}".format(results["label"]))
            insert_result()


        
        
else:
    st.warning("Prediçao ainda não realizada")