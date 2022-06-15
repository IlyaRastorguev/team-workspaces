id=$(docker create teamworkspaces)
docker cp $id:/vscode-reh-web-linux-x64 - > code.tar.gz
docker rm -v $id
