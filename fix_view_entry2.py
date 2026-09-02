import re

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "r") as f:
    text = f.read()

# Add ExperimentalFoundationApi
if "import androidx.compose.foundation.ExperimentalFoundationApi" not in text:
    text = text.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.ExperimentalFoundationApi\nimport androidx.compose.foundation.combinedClickable\nimport androidx.compose.material3.SnackbarHost\nimport androidx.compose.material3.SnackbarHostState\nimport kotlinx.coroutines.launch")

old_opt_in = "@OptIn(ExperimentalMaterial3Api::class)"
new_opt_in = "@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)"
text = text.replace(old_opt_in, new_opt_in)

old_scaffold_top = """    Scaffold(
        topBar = {"""
new_scaffold_top = """    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {"""
text = text.replace(old_scaffold_top, new_scaffold_top)

old_icon_spacing = """            }
                
            Spacer(modifier = Modifier.height(32.dp))
    
            Card("""

new_icon_spacing = """            }
                
            Spacer(modifier = Modifier.height(16.dp))
            Text(text = (entry[BasicField.Title]?.content ?: "") ?: "", fontWeight = FontWeight.Bold, fontSize = 24.sp)
            
            val urlContent = entry[BasicField.Url]?.content
            if (!urlContent.isNullOrBlank()) {
                Text(
                    text = urlContent,
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.combinedClickable(
                        onClick = { /* open link could go here */ },
                        onLongClick = {
                            clipboardManager.setText(AnnotatedString(urlContent))
                            scope.launch { snackbarHostState.showSnackbar("URL copied to clipboard") }
                        }
                    )
                )
            } else {
                Text(text = entry.customData["TemplateType"]?.value ?: "Entry", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }

            Spacer(modifier = Modifier.height(32.dp))
    
            Card("""
text = text.replace(old_icon_spacing, new_icon_spacing)

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "w") as f:
    f.write(text)

