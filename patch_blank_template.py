import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

# Make showUsername, showPassword, showUrl, showNotes default to false when creating a template
old_states = """    var showUsername by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_UserName"]?.value != "true" else true) }
    var showPassword by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Password"]?.value != "true" else true) }
    var showUrl by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Url"]?.value != "true" else true) }
    var showNotes by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Notes"]?.value != "true" else true) }"""

new_states = """    var showUsername by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_UserName"]?.value != "true" else !isTemplate) }
    var showPassword by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Password"]?.value != "true" else !isTemplate) }
    var showUrl by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Url"]?.value != "true" else !isTemplate) }
    var showNotes by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Notes"]?.value != "true" else !isTemplate) }"""

content = content.replace(old_states, new_states)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
