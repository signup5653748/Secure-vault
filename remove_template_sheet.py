import re

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

# Using regex to remove the `if (showTemplateSheet) { ... }` block
# Since we removed `showTemplateSheet`, this block will cause compile errors anyway.

pattern = r"            if \(showTemplateSheet\).*?Spacer\(modifier = Modifier\.height\(32\.dp\)\)\n                    \}\n                \}\n            \}"
content = re.sub(pattern, "", content, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)
