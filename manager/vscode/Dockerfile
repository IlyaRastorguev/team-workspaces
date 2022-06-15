FROM node:16

USER root

RUN git clone --depth 1 --branch 1.68.0 https://github.com/microsoft/vscode.git /editor

RUN chmod 777 /editor
RUN apt-get update && apt-get install python build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev -y
RUN mkdir -p /root/.vscode-server-oss-dev/data/logs
RUN node /editor/build/lib/preLaunch.js
RUN cd /editor && yarn gulp "vscode-reh-web-linux-x64"
