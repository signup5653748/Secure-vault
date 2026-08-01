import os

files_to_fix = [
    "app/src/main/java/com/example/ui/AboutScreen.kt",
    "app/src/main/java/com/example/ui/AddEntryScreen.kt",
    "app/src/main/java/com/example/ui/AddGroupScreen.kt",
    "app/src/main/java/com/example/ui/AddNoteScreen.kt",
    "app/src/main/java/com/example/ui/CreateDatabaseScreen.kt",
    "app/src/main/java/com/example/ui/SecureScreen.kt",
    "app/src/main/java/com/example/ui/SettingsScreen.kt",
    "app/src/main/java/com/example/ui/TemplatesScreen.kt",
    "app/src/main/java/com/example/ui/ViewEntryScreen.kt"
]

for filepath in files_to_fix:
    with open(filepath, "r") as f:
        content = f.read()
    
    if "import androidx.compose.material.icons.automirrored.filled.*" not in content:
        content = content.replace("import androidx.compose.material.icons.filled.*", "import androidx.compose.material.icons.filled.*\nimport androidx.compose.material.icons.automirrored.filled.*")
        
    with open(filepath, "w") as f:
        f.write(content)

print("Fixed imports")
