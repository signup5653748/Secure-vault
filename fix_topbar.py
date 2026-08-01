import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

content = content.replace("if (!viewModel.isRootGroup()) {", "if (!isRoot) {")

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
print("fixed topbar")
