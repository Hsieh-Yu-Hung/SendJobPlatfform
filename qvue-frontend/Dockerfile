# 使用 Nginx 作為反向代理
FROM nginx:alpine

# 設定工作目錄
WORKDIR /usr/share/nginx/html

# 移除預設的 Nginx 靜態文件
RUN rm -rf ./*

# 複製 nginx 設定檔
COPY nginx.conf /etc/nginx/nginx.conf

# 將 Vue 的靜態文件拷貝到 Nginx 的靜態資源目錄
COPY dist/ .

# 暴露容器的 80 端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# docker build -t vue-front-end:latest .
# docker run --name vue-front-end-container -d -p 7080:80 vue-front-end:latest
