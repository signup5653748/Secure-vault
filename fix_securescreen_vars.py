with open("app/src/main/java/com/example/ui/SecureScreen.kt", "r") as f:
    text = f.read()

import re

# Add sortOrder state correctly near the top of the composable
vars_old = """    val currentGroup by viewModel.currentGroup.collectAsState()
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)"""

vars_new = """    val currentGroup by viewModel.currentGroup.collectAsState()
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    var sortOrder by remember { mutableStateOf("Default") }
    var showSortMenu by remember { mutableStateOf(false) }"""

text = text.replace(vars_old, vars_new)

with open("app/src/main/java/com/example/ui/SecureScreen.kt", "w") as f:
    f.write(text)

print("Fixed vars")
