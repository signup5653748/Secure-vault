#!/bin/bash
awk '
/onNavigateToTemplates: \(\) -> Unit = \{\},/ {
    print "    onNavigateToEditGroup: () -> Unit = {},"
    print "    onNavigateToEditEntry: () -> Unit = {},"
    print $0
    next
}
{ print $0 }
' app/src/main/java/com/example/ui/VaultScreen.kt > app/src/main/java/com/example/ui/VaultScreen.kt.new
mv app/src/main/java/com/example/ui/VaultScreen.kt.new app/src/main/java/com/example/ui/VaultScreen.kt
