import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()
    
# We will use regex to find:
#                         if (isDeleteMode) {
#                             Column {
#                                 IconButton(onClick = { 
#                                     if (index > 0) { ... }
#                                 }) {
#                                     Icon(Icons.Default.KeyboardArrowUp, "Move Up")
#                                 }
#                                 IconButton(onClick = {
#                                     if (index < fieldOrder.size - 1) { ... }
#                                 }) {
#                                     Icon(Icons.Default.KeyboardArrowDown, "Move Down")
#                                 }
#                             }
#                             Checkbox(checked = selectedFieldsToDelete.contains("FIELD_NAME"), onCheckedChange = { checked -> ... })
#                         }

pattern = re.compile(r"""                        if \(isDeleteMode\) \{
                            Column \{
                                IconButton\(onClick = \{\s*
                                    if \(index > 0\) \{
                                        val mutableOrder = fieldOrder\.toMutableList\(\)
                                        val temp = mutableOrder\[index - 1\]
                                        mutableOrder\[index - 1\] = mutableOrder\[index\]
                                        mutableOrder\[index\] = temp
                                        fieldOrder = mutableOrder
                                    \}
                                \}\) \{
                                    Icon\(Icons\.Default\.KeyboardArrowUp, "Move Up"\)
                                \}
                                IconButton\(onClick = \{
                                    if \(index < fieldOrder\.size - 1\) \{
                                        val mutableOrder = fieldOrder\.toMutableList\(\)
                                        val temp = mutableOrder\[index \+ 1\]
                                        mutableOrder\[index \+ 1\] = mutableOrder\[index\]
                                        mutableOrder\[index\] = temp
                                        fieldOrder = mutableOrder
                                    \}
                                \}\) \{
                                    Icon\(Icons\.Default\.KeyboardArrowDown, "Move Down"\)
                                \}
                            \}
                            Checkbox\(checked = selectedFieldsToDelete\.contains\("([^"]+)"\), onCheckedChange = \{ checked ->
                                if \(checked\) selectedFieldsToDelete = selectedFieldsToDelete \+ "\1" else selectedFieldsToDelete = selectedFieldsToDelete - "\1"
                            \}\)
                        \}""")

def replacer(match):
    field_name = match.group(1)
    return f"""                        if (isDeleteMode) {{
                            Checkbox(checked = selectedFieldsToDelete.contains("{field_name}"), onCheckedChange = {{ checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "{field_name}" else selectedFieldsToDelete = selectedFieldsToDelete - "{field_name}"
                            }})
                        }}
                        if (isReorderMode) {{
                            Icon(
                                Icons.Default.DragHandle, 
                                contentDescription = "Reorder",
                                modifier = Modifier
                                    .padding(end = 8.dp)
                                    .pointerInput(Unit) {{
                                        detectDragGesturesAfterLongPress(
                                            onDrag = {{ change, dragAmount -> 
                                                change.consume()
                                                val threshold = 50f
                                                if (dragAmount.y > threshold && index < fieldOrder.size - 1) {{
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index + 1]
                                                    mutableOrder[index + 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                }} else if (dragAmount.y < -threshold && index > 0) {{
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index - 1]
                                                    mutableOrder[index - 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                }}
                                            }}
                                        )
                                    }}
                            )
                        }}"""

text = pattern.sub(replacer, text)

# Also need to replace the custom field part
pattern_custom = re.compile(r"""                        if \(isDeleteMode\) \{
                            Column \{
                                IconButton\(onClick = \{\s*
                                    if \(index > 0\) \{
                                        val mutableOrder = fieldOrder\.toMutableList\(\)
                                        val temp = mutableOrder\[index - 1\]
                                        mutableOrder\[index - 1\] = mutableOrder\[index\]
                                        mutableOrder\[index\] = temp
                                        fieldOrder = mutableOrder
                                    \}
                                \}\) \{
                                    Icon\(Icons\.Default\.KeyboardArrowUp, "Move Up"\)
                                \}
                                IconButton\(onClick = \{
                                    if \(index < fieldOrder\.size - 1\) \{
                                        val mutableOrder = fieldOrder\.toMutableList\(\)
                                        val temp = mutableOrder\[index \+ 1\]
                                        mutableOrder\[index \+ 1\] = mutableOrder\[index\]
                                        mutableOrder\[index\] = temp
                                        fieldOrder = mutableOrder
                                    \}
                                \}\) \{
                                    Icon\(Icons\.Default\.KeyboardArrowDown, "Move Down"\)
                                \}
                            \}
                            Checkbox\(checked = selectedFieldsToDelete\.contains\("Custom:\$\{customField\.name\}"\), onCheckedChange = \{ checked ->
                                if \(checked\) selectedFieldsToDelete = selectedFieldsToDelete \+ "Custom:\$\{customField\.name\}" else selectedFieldsToDelete = selectedFieldsToDelete - "Custom:\$\{customField\.name\}"
                            \}\)
                        \}""")

def replacer_custom(match):
    return f"""                        if (isDeleteMode) {{
                            Checkbox(checked = selectedFieldsToDelete.contains("Custom:${{customField.name}}"), onCheckedChange = {{ checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Custom:${{customField.name}}" else selectedFieldsToDelete = selectedFieldsToDelete - "Custom:${{customField.name}}"
                            }})
                        }}
                        if (isReorderMode) {{
                            Icon(
                                Icons.Default.DragHandle, 
                                contentDescription = "Reorder",
                                modifier = Modifier
                                    .padding(end = 8.dp)
                                    .pointerInput(Unit) {{
                                        detectDragGesturesAfterLongPress(
                                            onDrag = {{ change, dragAmount -> 
                                                change.consume()
                                                val threshold = 50f
                                                if (dragAmount.y > threshold && index < fieldOrder.size - 1) {{
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index + 1]
                                                    mutableOrder[index + 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                }} else if (dragAmount.y < -threshold && index > 0) {{
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index - 1]
                                                    mutableOrder[index - 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                }}
                                            }}
                                        )
                                    }}
                            )
                        }}"""

text = pattern_custom.sub(replacer_custom, text)

# Need to import detectDragGesturesAfterLongPress and pointerInput and DragHandle
imports = """import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.material.icons.filled.DragHandle
"""
if "detectDragGesturesAfterLongPress" not in text:
    text = text.replace("import androidx.compose.material.icons.filled.KeyboardArrowDown", "import androidx.compose.material.icons.filled.KeyboardArrowDown\n" + imports)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

print("Fixed fields")
