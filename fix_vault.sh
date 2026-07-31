#!/bin/bash
sed -i 's/onNavigateToEditGroup: () -> Unit = {},//g' app/src/main/java/com/example/ui/VaultScreen.kt
sed -i 's/onNavigateToEditEntry: () -> Unit = {},//g' app/src/main/java/com/example/ui/VaultScreen.kt
