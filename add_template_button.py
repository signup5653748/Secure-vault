import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

new_imports = """import androidx.compose.material3.TextButton
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import kotlinx.coroutines.launch
"""

content = content.replace("import androidx.compose.foundation.lazy.grid.items", "import androidx.compose.foundation.lazy.grid.items\n" + new_imports)

sheet_state = """    var showAttachmentsDialog by remember { mutableStateOf(false) }
    val clipboardManager: ClipboardManager = LocalClipboardManager.current
    
    var showTemplateSheet by remember { mutableStateOf(false) }
    val templateSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val templates = viewModel.getTemplates()
    val scope = rememberCoroutineScope()
"""
content = content.replace("""    var showAttachmentsDialog by remember { mutableStateOf(false) }
    val clipboardManager: ClipboardManager = LocalClipboardManager.current""", sheet_state)

top_bar_actions = """                title = { Text(if (isTemplate) "New Template" else "New Entry") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (!isTemplate) {
                        TextButton(onClick = { showTemplateSheet = true }) {
                            Text("Choose Template")
                        }
                    }
                }
"""

content = content.replace("""                title = { Text(if (isTemplate) "New Template" else "New Entry") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },""", top_bar_actions)

template_sheet = """            item { Spacer(modifier = Modifier.height(8.dp)) }"""

template_sheet_full = """            item { Spacer(modifier = Modifier.height(8.dp)) }
            
            if (showTemplateSheet) {
                ModalBottomSheet(
                    onDismissRequest = { showTemplateSheet = false },
                    sheetState = templateSheetState
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp)
                    ) {
                        Text("Select a template", fontSize = 20.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        LazyColumn {
                            items(templates.size) { index ->
                                val template = templates[index]
                                Card(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 8.dp)
                                        .clickable {
                                            title = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
                                            username = template[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
                                            url = template[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
                                            notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
                                            iconName = template.icon.name
                                            color = template.customData["ThemeColor"]?.value ?: "Blue"
                                            
                                            // Handle custom fields
                                            val newCustomFields = mutableListOf<CustomFieldData>()
                                            template.fields.entries.forEach { (key, value) ->
                                                if (key !is app.keemobile.kotpass.constants.BasicField) {
                                                    val fieldName = key.name
                                                    val isHidden = value is app.keemobile.kotpass.cryptography.EncryptedValue
                                                    val fieldValue = value.content
                                                    val showCopy = template.customData["ShowCopyButton_$fieldName"]?.value == "true"
                                                    newCustomFields.add(CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopy))
                                                }
                                            }
                                            customFields = newCustomFields
                                            
                                            scope.launch { templateSheetState.hide() }.invokeOnCompletion {
                                                if (!templateSheetState.isVisible) {
                                                    showTemplateSheet = false
                                                }
                                            }
                                        },
                                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                                ) {
                                    Row(
                                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        val iconColor = parseColor(template.customData["ThemeColor"]?.value)
                                        val iconVector = parseIcon(template.icon.name)
                                        Icon(iconVector, contentDescription = null, tint = iconColor, modifier = Modifier.size(32.dp))
                                        Spacer(modifier = Modifier.width(16.dp))
                                        Text(text = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: "Unnamed", fontSize = 18.sp)
                                    }
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                }
            }"""

content = content.replace(template_sheet, template_sheet_full)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)

