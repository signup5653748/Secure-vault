#!/bin/bash
awk '
/item \{/ && /var passVisible/ {
    print "            if (showPassword) {"
    print "                item {"
    print "                    var passVisible by remember { mutableStateOf(false) }"
    in_password = 1
    next
}
in_password && /item \{/ && /OutlinedTextField/ {
    print "                    }"
    print "                }"
    print "            }"
    print "            if (showUrl) {"
    print "                item {"
    print "                    Row(verticalAlignment = Alignment.CenterVertically) {"
    print "                        OutlinedTextField("
    print "                            value = url,"
    print "                            onValueChange = { url = it },"
    print "                            label = { Text(\"URL\") },"
    print "                            modifier = Modifier.weight(1f)"
    print "                        )"
    print "                        if (isTemplate || isEdit || !isTemplate) {"
    print "                            IconButton(onClick = { showUrl = false; url = \"\" }) {"
    print "                                Icon(Icons.Default.Delete, contentDescription = \"Remove URL\", tint = Color.Red)"
    print "                            }"
    print "                        }"
    print "                    }"
    print "                }"
    print "            }"
    in_password = 0
    in_url = 1
    next
}
in_url && /if \(showNotes\)/ {
    in_url = 0
    print $0
    next
}
in_url {
    # We are skipping the original URL item
    next
}
in_password && /modifier = Modifier.fillMaxWidth\(\)/ && !/clip/ {
    print "                            modifier = Modifier.weight(1f)"
    next
}
in_password && /if \(password.isNotEmpty\(\)\)/ {
    print "                        if (isTemplate || isEdit || !isTemplate) {"
    print "                            IconButton(onClick = { showPassword = false; password = \"\" }) {"
    print "                                Icon(Icons.Default.Delete, contentDescription = \"Remove Password\", tint = Color.Red)"
    print "                            }"
    print "                        }"
    print "                    }"
    print "                    if (password.isNotEmpty()) {"
    next
}
in_password && /Column\(modifier = Modifier.fillMaxWidth\(\)\)/ {
    print "                    Column(modifier = Modifier.fillMaxWidth()) {"
    print "                        Row(verticalAlignment = Alignment.CenterVertically) {"
    next
}
{ print $0 }
' app/src/main/java/com/example/ui/AddEntryScreen.kt > app/src/main/java/com/example/ui/AddEntryScreen.kt.new
mv app/src/main/java/com/example/ui/AddEntryScreen.kt.new app/src/main/java/com/example/ui/AddEntryScreen.kt
