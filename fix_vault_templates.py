import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# Add BottomSheet for choosing template
target = "if (showFabMenu) {"

replacement = """            if (showChooseTemplateSheet) {
                val templates = viewModel.getTemplates()
                ModalBottomSheet(
                    onDismissRequest = { showChooseTemplateSheet = false }
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp)
                    ) {
                        Text("Select a template", fontSize = 20.sp, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        androidx.compose.foundation.lazy.LazyColumn {
                            items(templates.size) { index ->
                                val template = templates[index]
                                Card(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 8.dp)
                                        .clickable {
                                            viewModel.selectTemplateForNewEntry(template)
                                            showChooseTemplateSheet = false
                                            onNavigateToAddEntry()
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
            if (showFabMenu) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
print("fixed templates sheet in vault")
