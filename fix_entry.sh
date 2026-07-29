#!/bin/bash
# Remove palette action from TopAppBar
sed -i '/actions = {/,/}/d' app/src/main/java/com/example/ui/AddEntryScreen.kt

# Replace showIconColorDialog with two new dialog states and predefined lists
sed -i 's/var showIconColorDialog by remember { mutableStateOf(false) }/var showIconDialog by remember { mutableStateOf(false) }\n    var showColorDialog by remember { mutableStateOf(false) }\n    val predefinedIcons = listOf("Key", "Folder", "Network", "Lock", "Email", "World", "Money", "Note")\n    val predefinedColors = listOf("Blue", "Red", "Green", "Yellow", "Cyan", "Magenta", "Gray", "Black", "White")/g' app/src/main/java/com/example/ui/AddEntryScreen.kt
