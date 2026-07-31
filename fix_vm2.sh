#!/bin/bash
awk '
/fun realSaveDatabase\(\) \{/ {
    print "    fun saveDatabase() {"
    print "        realSaveDatabase()"
    print "    }"
    print ""
    print $0
    next
}
{ print $0 }
' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt > app/src/main/java/com/example/viewmodel/KeePassViewModel.kt.new
mv app/src/main/java/com/example/viewmodel/KeePassViewModel.kt.new app/src/main/java/com/example/viewmodel/KeePassViewModel.kt
