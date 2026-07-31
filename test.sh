#!/bin/bash
unzip -q -c ~/.gradle/caches/modules-2/files-2.1/app.keemobile.kotpass/kotpass-core-jvm/*/kotpass-core-jvm-*.jar \
| grep -a "KeePassDatabase"
