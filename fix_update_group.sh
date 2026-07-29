#!/bin/bash
sed -i 's/val newCurrentGroup = updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first/val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first/g' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt
