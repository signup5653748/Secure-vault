import re

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "r") as f:
    text = f.read()

# Add the Title and Subtitle back below the Icon
old_icon_spacing = """            }
                
            Spacer(modifier = Modifier.height(32.dp))
    
            Card("""

new_icon_spacing = """            }
                
            Spacer(modifier = Modifier.height(16.dp))
            Text(text = (entry[BasicField.Title]?.content ?: "") ?: "", fontWeight = FontWeight.Bold, fontSize = 24.sp)
            
            val urlContent = entry[BasicField.Url]?.content
            val subtitleText = if (!urlContent.isNullOrBlank()) urlContent else (entry.customData["TemplateType"]?.value ?: "Entry")
            Text(text = subtitleText, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)

            Spacer(modifier = Modifier.height(32.dp))
    
            Card("""

text = text.replace(old_icon_spacing, new_icon_spacing)

# Remove the URL row from the Card
old_url_row = """                    if (entry.fields.containsKey(BasicField.Url()) && !(entry[BasicField.Url]?.content ?: "").isNullOrEmpty()) {
                        ViewFieldRow(
                            icon = Icons.Default.Link,
                            text = (entry[BasicField.Url]?.content ?: ""),
                            onCopy = { clipboardManager.setText(AnnotatedString((entry[BasicField.Url]?.content ?: ""))) }
                        )
                        HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                    }"""

new_url_row = """"""

text = text.replace(old_url_row, new_url_row)

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "w") as f:
    f.write(text)

print("Updated ViewEntryScreen")
