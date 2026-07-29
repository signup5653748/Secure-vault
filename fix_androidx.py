with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

content = content.replace("androidx.compose.foundation.layout.", "")
content = content.replace("androidx.compose.ui.", "")
content = content.replace("androidx.compose.material3.", "")
content = content.replace("androidx.compose.foundation.", "")
content = content.replace("androidx.compose.ui.text.font.", "")

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
