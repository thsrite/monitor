FROM python:3.9-slim
ENV TZ=Asia/Shanghai
WORKDIR ./monitor
ADD . .
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]