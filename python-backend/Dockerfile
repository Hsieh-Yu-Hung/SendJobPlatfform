# 使用 python:3.12-slim 作為基礎映像檔
FROM python:3.12-slim

# Switch to root user
USER root

# 複製認證文件到容器內
COPY gcloud /root/.config/gcloud

# 安裝 lsb-release 以便使用 lsb_release 指令
RUN apt-get update && apt-get install -y lsb-release

# 安裝 gcsfuse
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb http://packages.cloud.google.com/apt gcsfuse-$(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gcsfuse.list && \
    apt-get update && \
    apt-get install -y gcsfuse && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 添加 Google Cloud SDK 的套件來源
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# 安裝 Google Cloud SDK 
RUN apt-get update && apt-get install -y google-cloud-sdk && apt-get install -y git && apt-get clean  

# Set working directory
WORKDIR /app
COPY . /app
RUN mkdir -p /app/data

# 設置環境變量
ENV GOOGLE_APPLICATION_CREDENTIALS="/root/.config/gcloud/application_default_credentials.json"
ENV PYTHONPATH="/app"

# 安裝 requirements.txt 中的 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 API 的 port
EXPOSE 5987
EXPOSE 5988

# Execute the script with the SAMPLE_ID environment variable
CMD ["bash", "initiateAPI.sh"]

#
# docker build -t python-backend .
# docker run -d --name python-backend-container -v /Users/yu-hung/Desktop/TestingGround/Send_JOB_Platform/data:/app/data -p 5987:5987 -p 5988:5988 python-backend