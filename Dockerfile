FROM python:3.7
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod a+x /app
EXPOSE 3000
CMD ["gunicorn", "--workers=16", "-b 0.0.0.0:3000","app_main:core"]