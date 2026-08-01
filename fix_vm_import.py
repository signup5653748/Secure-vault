import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

# Add BasicField import
if "import app.keemobile.kotpass.constants.BasicField" not in text:
    text = text.replace("import androidx.lifecycle.viewModelScope", "import androidx.lifecycle.viewModelScope\nimport app.keemobile.kotpass.constants.BasicField")
    with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
        f.write(text)

