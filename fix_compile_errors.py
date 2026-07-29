import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

# Fix 1: Move ModalBottomSheet outside LazyColumn
# Currently it's at: 
#             item { Spacer(modifier = Modifier.height(8.dp)) }
#             
#             if (showTemplateSheet) { ...

pattern = r"            if \(showTemplateSheet\) \{\n                ModalBottomSheet\(.*?Spacer\(modifier = Modifier\.height\(32\.dp\)\)\n                    \}\n                \}\n            \}"
sheet_code = re.search(pattern, content, flags=re.DOTALL)
if sheet_code:
    content = content.replace(sheet_code.group(0), "")
    # Add it before the main Scaffold closing bracket or outside the LazyColumn
    # It's inside the Scaffold's content block: `) { paddingValues -> \n LazyColumn ... }`
    # Let's place it after the LazyColumn
    
    # We'll just replace the last closing brace of the Scaffold content block with the sheet + closing brace
    content = content.replace("        }\n    }\n}", "        }\n" + sheet_code.group(0).replace("            if", "        if") + "\n    }\n}")

# Fix 2: Fix key !is BasicField
old_key_check = """                                                if (key !is app.keemobile.kotpass.constants.BasicField) {
                                                    val fieldName = key.name"""
new_key_check = """                                                val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
                                                if (key !in basicFields) {
                                                    val fieldName = key"""

content = content.replace(old_key_check, new_key_check)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content_vm = f.read()

content_vm = content_vm.replace("copy(groups = entries + newEntry)", "copy(entries = entries + newEntry)")

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content_vm)

