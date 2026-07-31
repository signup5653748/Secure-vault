import sys

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

target = """                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Green"),
                        "Hide_Url" to app.keemobile.kotpass.models.CustomDataValue("true")"""
replacement = """                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Green"),
                        "Hide_Url" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_UserName" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Password" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Notes" to app.keemobile.kotpass.models.CustomDataValue("true")"""

new_content = content.replace(target, replacement)
with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(new_content)
print("Fixed VM")
