FROM python:3.12-alpine
WORKDIR app/
COPY . .
RUN pip install -r requirements.txt
CMD python main.py

#Terminalda run qilish uchun ->
#-> docker build -t image_name  :version  image_name kichik bolishi kerak
#-> docker build -t GYM:latest
