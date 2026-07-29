import re

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

# Remove the template FAB from VaultScreen
old_fab_menu = """                        if (showFabMenu) {
                            ExtendedFloatingActionButton(
                                text = { Text("Template") },
                                icon = { Icon(Icons.Default.LibraryAdd, "Template") },
                                onClick = { 
                                    showFabMenu = false
                                    showTemplateSheet = true
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                            ExtendedFloatingActionButton("""

new_fab_menu = """                        if (showFabMenu) {
                            ExtendedFloatingActionButton("""

content = content.replace(old_fab_menu, new_fab_menu)

# Also remove showTemplateSheet from VaultScreen as it's not used there anymore
content = content.replace("    var showTemplateSheet by remember { mutableStateOf(false) }", "")
content = content.replace("    val templateSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)", "")

# Wait, the template bottom sheet was originally in VaultScreen, so let's remove it if it exists.
# We will use regex to remove the modal bottom sheet for templates if it exists in VaultScreen.

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)

