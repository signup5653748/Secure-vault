#!/bin/bash
sed -i 's/fun saveDatabase/fun realSaveDatabase/g' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt
sed -i 's/\/\/ \/\/ saveDatabase()/\/\/ saveDatabase()/g' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt
sed -i 's/fun lockDatabase() {/fun lockDatabase() {\n        realSaveDatabase()\n/g' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt
