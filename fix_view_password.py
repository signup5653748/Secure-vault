import re

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "r") as f:
    text = f.read()

old_pwd = """                    // Password Row
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.VpnKey,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(
                            text = if (passwordVisible) (entry[BasicField.Password]?.content ?: "") else "••••••••••••",
                            modifier = Modifier.weight(1f),
                            fontSize = 16.sp
                        )
                        IconButton(onClick = { passwordVisible = !passwordVisible }) {
                            Icon(
                                if (passwordVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                contentDescription = if (passwordVisible) "Hide password" else "Show password"
                            )
                        }
                        IconButton(onClick = { clipboardManager.setText(AnnotatedString((entry[BasicField.Password]?.content ?: ""))) }) {
                            Icon(Icons.Default.ContentCopy, contentDescription = "Copy Password")
                        }
                    }"""

new_pwd = """                    // Password Row
                    if (entry.fields.containsKey(BasicField.Password())) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                Icons.Default.VpnKey,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(16.dp))
                            Text(
                                text = if (passwordVisible) (entry[BasicField.Password]?.content ?: "") else "••••••••••••",
                                modifier = Modifier.weight(1f),
                                fontSize = 16.sp
                            )
                            IconButton(onClick = { passwordVisible = !passwordVisible }) {
                                Icon(
                                    if (passwordVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                    contentDescription = if (passwordVisible) "Hide password" else "Show password"
                                )
                            }
                            IconButton(onClick = { clipboardManager.setText(AnnotatedString((entry[BasicField.Password]?.content ?: ""))) }) {
                                Icon(Icons.Default.ContentCopy, contentDescription = "Copy Password")
                            }
                        }
                    }"""

text = text.replace(old_pwd, new_pwd)

old_url = """                    if (!(entry[BasicField.Url]?.content ?: "").isNullOrEmpty()) {"""
new_url = """                    if (entry.fields.containsKey(BasicField.Url()) && !(entry[BasicField.Url]?.content ?: "").isNullOrEmpty()) {"""
text = text.replace(old_url, new_url)

old_user = """                    if (!(entry[BasicField.UserName]?.content ?: "").isNullOrEmpty()) {"""
new_user = """                    if (entry.fields.containsKey(BasicField.UserName()) && !(entry[BasicField.UserName]?.content ?: "").isNullOrEmpty()) {"""
text = text.replace(old_user, new_user)

old_notes = """            if (!(entry[BasicField.Notes]?.content ?: "").isNullOrEmpty()) {
                Spacer(modifier = Modifier.height(32.dp))
                Text(text = "Notes", fontWeight = FontWeight.SemiBold, fontSize = 18.sp, modifier = Modifier.fillMaxWidth())
                Spacer(modifier = Modifier.height(8.dp))
                Card(
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
new_notes = """            if (entry.fields.containsKey(BasicField.Notes()) && !(entry[BasicField.Notes]?.content ?: "").isNullOrEmpty()) {
                Spacer(modifier = Modifier.height(32.dp))
                Text(text = "Notes", fontWeight = FontWeight.SemiBold, fontSize = 18.sp, modifier = Modifier.fillMaxWidth())
                Spacer(modifier = Modifier.height(8.dp))
                Card(
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
text = text.replace(old_notes, new_notes)

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "w") as f:
    f.write(text)

