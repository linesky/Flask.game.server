
from flask import Flask, render_template, Response
from PIL import Image, ImageDraw
import io
import time
import threading

app = Flask(__name__)

# Inicializar variáveis de animação
frame_rate = 30  # 30 frames por segundo
circle_pos = 100
direction = 1
image_width = 640
image_height = 480
circle_radius = 15

def generate_image():
    global circle_pos, direction
    while True:
        # Criar uma nova imagem
        image = Image.new("RGB", (image_width, image_height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Desenhar um círculo
        circle_x = circle_pos
        circle_y = image_height // 2
        draw.ellipse((circle_x - circle_radius, circle_y - circle_radius, 
                      circle_x + circle_radius, circle_y + circle_radius), 
                     fill=(0, 0, 255), outline=(0, 0, 0))

        # Atualizar a posição do círculo
        circle_pos += direction * 5
        if circle_pos >630 or circle_pos<40:
            direction *= -1

        # Converter a imagem para bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Enviar a imagem como stream
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + img_byte_arr + b'\r\n')
        
        time.sleep(1 / frame_rate)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_image(), mimetype='multipart/x-mixed-replace; boundary=frame')
print("\x1bc\x1b[47;34m")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
