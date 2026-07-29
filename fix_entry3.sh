#!/bin/bash
sed -i '/if (showIconColorDialog) {/,/    }/d' app/src/main/java/com/example/ui/AddEntryScreen.kt

cat app/src/main/java/com/example/ui/AddGroupScreen.kt | awk '
/if \(showIconDialog\) \{/ {p=1}
/if \(showColorDialog\) \{/ {c=1}
p==1 {print; if ($0 == "        }") {p=0}}
c==1 && p==0 {print; if ($0 == "        }") {c=0; exit}}
' > dialogs.txt

sed -i '/if (showAttachmentsDialog) {/i \
\n#INSERT_DIALOGS_HERE\n' app/src/main/java/com/example/ui/AddEntryScreen.kt

sed -i -e '/#INSERT_DIALOGS_HERE/r dialogs.txt' -e '/#INSERT_DIALOGS_HERE/d' app/src/main/java/com/example/ui/AddEntryScreen.kt
