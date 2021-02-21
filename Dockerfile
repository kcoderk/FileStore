FROM python:3.7.10
WORKDIR /app
COPY templates ./templates
COPY app.py ./

RUN pip install flask -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
EXPOSE 5000
CMD python app.py