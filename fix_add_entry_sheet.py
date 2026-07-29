import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

new_state = """    val clipboardManager: ClipboardManager = LocalClipboardManager.current

    var showTemplateSheet by remember { mutableStateOf(false) }
    val templateSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val templates = viewModel.getTemplates()
    val scope = rememberCoroutineScope()
"""

content = content.replace("    val clipboardManager: ClipboardManager = LocalClipboardManager.current", new_state)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
