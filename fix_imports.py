import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

if "import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress" not in text:
    text = text.replace("import androidx.compose.material.icons.filled.KeyboardArrowUp", "import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress\nimport androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.material.icons.filled.DragHandle\nimport androidx.compose.material.icons.filled.KeyboardArrowUp")
    
with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

print("Fixed imports")
