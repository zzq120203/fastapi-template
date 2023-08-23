FROM python:3.10-slim-buster

WORKDIR /app

# 时区设置
COPY build/Shanghai /usr/share/zoneinfo/Asia/Shanghai
RUN rm /etc/localtime; ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ENV TZ="Asia/Shanghai"

# python 环境设置
ENV LANG=C.UTF-8 PYTHONIOENCODING=utf-8 PYTHONPATH=/app

COPY ["build/requirements.txt", "build/fastapi_plugin-0.2.2-py3-none-any.whl", "./pypi/"]
RUN pip3 install -r pypi/requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN pip3 install pypi/fastapi_plugin-0.2.2-py3-none-any.whl[users] -i https://mirrors.aliyun.com/pypi/simple

COPY . /app

EXPOSE 8000

ENTRYPOINT ["python", "-u", "-m", "uvicorn", "app:app", "--log-config", "lib/ulogger.json", "--host", "0.0.0.0", "--port", "8000"]