#!/bin/bash
sed -i '/import androidx.compose.runtime.getValue/a import androidx.activity.compose.BackHandler' app/src/main/java/com/example/ui/VaultScreen.kt

# Inject BackHandler inside VaultScreen
sed -i '/val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)/a \
    BackHandler(enabled = !viewModel.isRootGroup()) {\n\
        viewModel.navigateUp()\n\
    }' app/src/main/java/com/example/ui/VaultScreen.kt

# Also change Icons.Default.ArrowBack to Icons.AutoMirrored.Filled.ArrowBack in VaultScreen
sed -i 's/Icons.Default.ArrowBack/Icons.AutoMirrored.Filled.ArrowBack/g' app/src/main/java/com/example/ui/VaultScreen.kt
