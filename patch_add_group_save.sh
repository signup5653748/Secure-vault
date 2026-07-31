#!/bin/bash
sed -i 's/viewModel.createGroup(title, iconName, color)/if (isEdit \&\& currentGroup != null) { viewModel.updateGroup(currentGroup!!, title, iconName, color) } else { viewModel.createGroup(title, iconName, color) }/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
