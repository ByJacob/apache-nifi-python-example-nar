#!/usr/bin/env bash

echo "Clear work directory and recreate"
rm -rf ./python_processor/tmp
mkdir -p ./python_processor/tmp


echo "Create MANIFEST.MF file"
mkdir -p ./python_processor/tmp/META-INF
cat > ./python_processor/tmp/META-INF/MANIFEST.MF << EOF
Manifest-Version: 1.0
Nifi-Dependency-Group: org.apache.nifi
Nifi-Dependency-Id: nifi-api
Nifi-Dependency-Version: 2.0.0
Nar-Id: my-nifi-python-nar
Nar-Group: com.example
Nar-Version: 1.0.0
Build-Tag: $(date +%s)
Build-Timestamp: $(date +%Y-%m-%dT%H:%M:%S%z)
Build-Revision: $(git rev-parse --short HEAD)
Build-Branch: $(git rev-parse --abbrev-ref HEAD)
Built-By: Script
Created-By: $(echo $USER)
EOF

echo "Create directory for dependencies"
mkdir -p ./python_processor/tmp/NAR-INF/bundled-dependencies

echo "Run inside nifi docker install pip requirements"

docker run -i --rm --userns=host --network=host --entrypoint /home/nifi/.local/bin/uv \
      -v ${PWD}/python_processor:/python_processor \
      apache/nifi:2.6.0 \
      pip install --no-cache-dir --link-mode=copy --upgrade debug --target /python_processor/tmp/NAR-INF/bundled-dependencies -r /python_processor/requirements.txt

echo "Copy python files to working directory"

cp ./python_processor/*.py ./python_processor/tmp

echo "Create nar extension"

rm -rf nifi-data/nar_extensions/my-python.nar
cd ./python_processor/tmp
zip -r ./../../nifi-data/nar_extensions/my-python.nar .
cd -