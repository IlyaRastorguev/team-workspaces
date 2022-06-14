FROM python:3.9

USER root

COPY vscode/code.tar.gz /code.tar.gz

RUN tar -xf code.tar.gz && rm code.tar.gz

RUN chmod 777 /vscode-reh-web-linux-x64
RUN mkdir -p /root/.vscode-server-oss-dev/data/logs

EXPOSE 9888

CMD ["/vscode-reh-web-linux-x64/node", "/vscode-reh-web-linux-x64/out/server-main.js", "--host", "0.0.0.0", "--without-connection-token"]
