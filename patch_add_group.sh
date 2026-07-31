#!/bin/bash
sed -i 's/onNavigateBack: () -> Unit/onNavigateBack: () -> Unit,\n    isEdit: Boolean = false/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/var title by remember { mutableStateOf("") }/val currentGroup by viewModel.currentGroup.collectAsState()\n    var title by remember { mutableStateOf(if (isEdit \&\& currentGroup != null) currentGroup!!.name else "") }/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/var iconName by remember { mutableStateOf("Folder") }/var iconName by remember { mutableStateOf(if (isEdit \&\& currentGroup != null) currentGroup!!.icon.name else "Folder") }/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/var color by remember { mutableStateOf("Blue") }/var color by remember { mutableStateOf(if (isEdit \&\& currentGroup != null) currentGroup!!.customData["ThemeColor"]?.value ?: "Blue" else "Blue") }/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
