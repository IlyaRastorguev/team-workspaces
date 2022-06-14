FROM node:16

USER root

COPY vscode /editor

RUN chmod 777 /editor
RUN apt-get update && apt-get install python build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev -y
RUN mkdir -p /root/.vscode-server-oss-dev/data/logs
RUN node /editor/build/lib/preLaunch.js
RUN cd /editor && yarn gulp "vscode-reh-web-linux-x64"

RUN rm -r /editor
RUN rm -r /tmp
RUN npm cache clean –force

CMD ["node", "/vscode-reh-web-linux-x64/out/server-main.js", "--host", "0.0.0.0"]
