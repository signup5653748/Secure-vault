import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# Update GroupItem
new_group_item = """@Composable
fun GroupItem(group: Group, onClick: () -> Unit) {
    val iconColor = parseColor(group.customData["ThemeColor"]?.value)
    val iconVector = parseIcon(group.icon.name)
    
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(vertical = 12.dp)
    ) {
        Icon(
            iconVector,
            contentDescription = "Folder",
            tint = iconColor,
            modifier = Modifier.size(24.dp)
        )
        Spacer(modifier = Modifier.width(16.dp))
        Text(text = group.name, fontSize = 16.sp)
    }
}"""
content = re.sub(r'@Composable\s*fun GroupItem\(group: Group, onClick: \(\) -> Unit\) \{.*?\n\}', new_group_item, content, flags=re.DOTALL)

# Update EntryItem
new_entry_item = """@Composable
fun EntryItem(entry: Entry, onClick: () -> Unit) {
    val iconColor = parseColor(entry.customData["ThemeColor"]?.value)
    val iconVector = parseIcon(entry.icon.name)

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                iconVector,
                contentDescription = "Key",
                tint = iconColor,
                modifier = Modifier.size(32.dp)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(text = (entry[BasicField.Title]?.content ?: ""), fontWeight = FontWeight.Medium, fontSize = 18.sp)
                if ((entry[BasicField.UserName]?.content ?: "").isNotEmpty()) {
                    Text(text = (entry[BasicField.UserName]?.content ?: ""), fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}"""
content = re.sub(r'@Composable\s*fun EntryItem\(entry: Entry, onClick: \(\) -> Unit\) \{.*?\n\}', new_entry_item, content, flags=re.DOTALL)

# Update the "New Group" dialog slightly to be real fields
new_dialog = """                            OutlinedTextField(
                                value = groupName,
                                onValueChange = { groupName = it },
                                label = { Text("Group Name") }
                            )
                            OutlinedTextField(
                                value = groupIcon,
                                onValueChange = { groupIcon = it },
                                label = { Text("Group Icon") },
                                modifier = Modifier.padding(top = 8.dp)
                            )
                            OutlinedTextField(
                                value = groupColor,
                                onValueChange = { groupColor = it },
                                label = { Text("Group Color") },
                                modifier = Modifier.padding(top = 8.dp)
                            )"""
content = content.replace("""                            OutlinedTextField(
                                value = groupName,
                                onValueChange = { groupName = it },
                                label = { Text("Group Name") }
                            )
                            // Placeholder for Icon & Color picker
                            Text("Icon: $groupIcon", modifier = Modifier.padding(top = 8.dp))
                            Text("Color: $groupColor")""", new_dialog)

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
