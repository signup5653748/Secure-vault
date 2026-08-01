with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

target = "import androidx.compose.ui.text.input.VisualTransformation"
new_imports = "import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress\nimport androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.material.icons.filled.DragHandle"

if "import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress" not in text:
    text = text.replace(target, target + "\n" + new_imports)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

print("Fixed imports for real real")
