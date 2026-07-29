import re

with open('/app/applet/app/src/main/java/com/example/ui/ViewEntryScreen.kt', 'r') as f:
    content = f.read()

# Make sure to import missing icons
import_stmt = "import androidx.compose.foundation.layout.*"
new_imports = """import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.filled.Label
import androidx.compose.material.icons.filled.Attachment
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items"""

if "import androidx.compose.material.icons.filled.Label" not in content:
    content = content.replace(import_stmt, new_imports)

old_notes_end = """                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Text(
                        text = (entry[BasicField.Notes]?.content ?: ""),
                        modifier = Modifier.padding(16.dp),
                        fontSize = 16.sp
                    )
                }
            }"""

new_tags_and_attachments = """                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Text(
                        text = (entry[BasicField.Notes]?.content ?: ""),
                        modifier = Modifier.padding(16.dp),
                        fontSize = 16.sp
                    )
                }
            }

            if (entry.tags.isNotEmpty()) {
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = "Tags",
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.align(Alignment.Start),
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(8.dp))
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    items(entry.tags) { tag ->
                        AssistChip(
                            onClick = { },
                            label = { Text(tag) },
                            leadingIcon = { Icon(Icons.Default.Label, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        )
                    }
                }
            }
            
            if (entry.binaries.isNotEmpty()) {
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = "Attachments",
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.align(Alignment.Start),
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(8.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Column {
                        entry.binaries.forEachIndexed { index, binaryRef ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    Icons.Default.Attachment,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Spacer(modifier = Modifier.width(16.dp))
                                Text(text = binaryRef.hash.hash, modifier = Modifier.weight(1f), fontSize = 16.sp, maxLines = 1)
                            }
                            if (index < entry.binaries.size - 1) {
                                HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                            }
                        }
                    }
                }
            }"""

content = content.replace(old_notes_end, new_tags_and_attachments)

with open('/app/applet/app/src/main/java/com/example/ui/ViewEntryScreen.kt', 'w') as f:
    f.write(content)
