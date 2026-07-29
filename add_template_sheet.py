import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

template_sheet = """
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
                                        
                                        val newCustomFields = mutableListOf<CustomFieldData>()
                                        val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
                                        template.fields.entries.forEach { (key, value) ->
                                            if (key !in basicFields) {
                                                val fieldName = key
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
        }
    }
}
"""

# replace the last "    }\n}" with template_sheet
content = content.rsplit("    }\n}", 1)[0] + template_sheet

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)

