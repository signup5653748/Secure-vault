import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# We need to make sure VaultScreen is closed properly before GroupItem
# Find @Composable fun GroupItem
idx = content.find("@Composable\nfun GroupItem")
if idx == -1:
    idx = content.find("@Composable\nfun GroupItem")

vault_screen_content = content[:idx]
rest_content = content[idx:]

# Count braces in vault_screen_content
open_b = vault_screen_content.count("{")
close_b = vault_screen_content.count("}")

print(f"VaultScreen braces - Open: {open_b}, Close: {close_b}")

if open_b > close_b:
    vault_screen_content += "}\n" * (open_b - close_b)

# Clean up excessive } at the end of rest_content if any
rest_content = rest_content.rstrip()
while rest_content.endswith("}"):
    rest_content = rest_content[:-1].rstrip()

# Now GroupItem and EntryItem each need to be closed properly.
# They were originally well-formed. I will just replace them with known good versions.

good_rest = """
@Composable
fun GroupItem(group: app.keemobile.kotpass.models.Group, onClick: () -> Unit) {
    val iconColor = parseColor(group.customData["ThemeColor"]?.value)
    val iconVector = parseIcon(group.icon.name)
    
    androidx.compose.foundation.layout.Row(
        verticalAlignment = androidx.compose.ui.Alignment.CenterVertically,
        modifier = androidx.compose.ui.Modifier
            .androidx.compose.foundation.layout.fillMaxWidth()
            .androidx.compose.foundation.clickable(onClick = onClick)
            .androidx.compose.foundation.layout.padding(vertical = 12.dp)
    ) {
        androidx.compose.material3.Icon(
            iconVector,
            contentDescription = "Folder",
            tint = iconColor,
            modifier = androidx.compose.ui.Modifier.androidx.compose.foundation.layout.size(24.dp)
        )
        androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.androidx.compose.foundation.layout.width(16.dp))
        androidx.compose.material3.Text(text = group.name, fontSize = 16.sp)
    }
}

@Composable
fun EntryItem(entry: app.keemobile.kotpass.models.Entry, onClick: () -> Unit) {
    val iconColor = parseColor(entry.customData["ThemeColor"]?.value)
    val iconVector = parseIcon(entry.icon.name)

    androidx.compose.material3.Card(
        modifier = androidx.compose.ui.Modifier
            .androidx.compose.foundation.layout.fillMaxWidth()
            .androidx.compose.foundation.clickable(onClick = onClick),
        colors = androidx.compose.material3.CardDefaults.cardColors(containerColor = androidx.compose.material3.MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        androidx.compose.foundation.layout.Row(
            modifier = androidx.compose.ui.Modifier
                .androidx.compose.foundation.layout.padding(16.dp)
                .androidx.compose.foundation.layout.fillMaxWidth(),
            verticalAlignment = androidx.compose.ui.Alignment.CenterVertically
        ) {
            androidx.compose.material3.Icon(
                iconVector,
                contentDescription = "Key",
                tint = iconColor,
                modifier = androidx.compose.ui.Modifier.androidx.compose.foundation.layout.size(32.dp)
            )
            androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.androidx.compose.foundation.layout.width(16.dp))
            androidx.compose.foundation.layout.Column {
                androidx.compose.material3.Text(text = (entry[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""), fontWeight = androidx.compose.ui.text.font.FontWeight.Medium, fontSize = 18.sp)
                if ((entry[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: "").isNotEmpty()) {
                    androidx.compose.material3.Text(text = (entry[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""), fontSize = 14.sp, color = androidx.compose.material3.MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}
"""

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(vault_screen_content + good_rest)
