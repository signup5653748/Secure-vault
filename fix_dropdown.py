import re

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

# Replace DropdownMenu for GroupItem and EntryItem
old_dropdown = """        DropdownMenu(
            expanded = showMenu,
            onDismissRequest = { showMenu = false }
        ) {"""

new_dropdown = """        Box(modifier = Modifier.fillMaxSize().wrapContentSize(Alignment.TopEnd)) {
            DropdownMenu(
                expanded = showMenu,
                onDismissRequest = { showMenu = false }
            ) {"""

# For GroupItem and EntryItem, the dropdown starts like old_dropdown.
# Then we need to add a closing brace `}` after the dropdown closing brace `}`.
# Actually, it's easier to use regex.

# We'll replace the block from DropdownMenu up to its closing brace.
def replace_dropdown(match):
    original = match.group(0)
    modified = "Box(modifier = Modifier.fillMaxSize().wrapContentSize(Alignment.TopEnd)) {\n    " + original.replace('\n', '\n    ') + "\n}"
    return modified

content = re.sub(r'DropdownMenu\(\s*expanded = showMenu,.*?}\s*\)\s*{.*?DropdownMenuItem.*?DropdownMenuItem.*?DropdownMenuItem.*?}\s*}\s*}', 
                 lambda m: "Box(modifier = Modifier.fillMaxSize().wrapContentSize(Alignment.TopEnd)) {\n        " + m.group(0) + "\n        }", 
                 content, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)

