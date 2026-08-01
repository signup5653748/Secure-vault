import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

target = """                            ExtendedFloatingActionButton(
                                text = { Text("Add group") },
                                icon = { Icon(Icons.Default.Folder, "Add group") },
                                onClick = {
                                    showFabMenu = false
                                    onNavigateToAddGroup()
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )"""

replacement = """                            ExtendedFloatingActionButton(
                                text = { Text("Add from Template") },
                                icon = { Icon(Icons.Default.ContentPaste, "Add from Template") },
                                onClick = {
                                    showFabMenu = false
                                    showChooseTemplateSheet = true
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
""" + target

content = content.replace(target, replacement)

# Add state for showChooseTemplateSheet
target2 = "var showFabMenu by remember { mutableStateOf(false) }"
replacement2 = "var showFabMenu by remember { mutableStateOf(false) }\n    var showChooseTemplateSheet by remember { mutableStateOf(false) }"
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
print("fixed fab again")
