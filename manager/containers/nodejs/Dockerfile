FROM node:16

USER root

ENV GIT_SSL_NO_VERIFY=1

ARG repo
ARG project_name

COPY vscode/code.tar.gz /code.tar.gz

RUN tar -xf code.tar.gz && rm code.tar.gz

RUN chmod 777 /vscode-reh-web-linux-x64
RUN mkdir -p /root/.vscode-server-oss-dev/data/logs

RUN git clone ${repo} ${project_name}

EXPOSE 8000

CMD ["node", "/vscode-reh-web-linux-x64/out/server-main.js", "--host", "0.0.0.0", "--without-connection-token"]
