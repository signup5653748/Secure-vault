#!/bin/bash
sed -i 's/fun \/\/ saveDatabase()/fun realSaveDatabase()/g' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt
