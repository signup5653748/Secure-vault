import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

# Fix conflicting fieldOrder
lines = text.split('\n')
seen = False
new_lines = []
for line in lines:
    if "var fieldOrder by remember(currentEntry?.uuid) { mutableStateOf(listOf(\"Username\", \"Password\", \"URL\", \"Notes\")) }" in line:
        if not seen:
            seen = True
            new_lines.append(line)
        else:
            pass # skip duplicate
    else:
        new_lines.append(line)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write('\n'.join(new_lines))

print("Fixed conflicting vars")
