
# 使用python3作为基础镜像
FROM python:3.10

# 设置工作目录为/app
WORKDIR /app

# 将当前目录下的所有文件复制到/app目录下
COPY . /app

# 安装依赖包
RUN pip install -r requirements.txt
# 暴露5000端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=main.py

# 运行程序
CMD ["flask", "run", "--host=0.0.0.0"]