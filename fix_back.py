import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

content = content.replace("BackHandler(enabled = !viewModel.isRootGroup()) {", "val isRoot = currentGroup?.uuid == database?.content?.group?.uuid\n    BackHandler(enabled = !isRoot) {")

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
print("fixed back")
