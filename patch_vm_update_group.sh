#!/bin/bash
awk '
/fun createGroup\(/ {
    print "    fun updateGroup(group: app.keemobile.kotpass.models.Group, name: String, iconName: String, color: String) {"
    print "        val currentDb = _database.value ?: return"
    print "        val currentGroup = _currentGroup.value ?: return"
    print "        val icon = try {"
    print "            app.keemobile.kotpass.constants.PredefinedIcon.valueOf(iconName)"
    print "        } catch (e: Exception) {"
    print "            app.keemobile.kotpass.constants.PredefinedIcon.Folder"
    print "        }"
    print "        val updatedGroup = group.copy("
    print "            name = name,"
    print "            icon = icon,"
    print "            customData = group.customData.toMutableMap().apply {"
    print "                put(\"ThemeColor\", app.keemobile.kotpass.models.CustomDataValue(color))"
    print "            }"
    print "        )"
    print "        val newCurrentGroup = currentGroup.copy(groups = currentGroup.groups.filter { it.uuid != group.uuid } + updatedGroup)"
    print "        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {"
    print "            copy(groups = groups.filter { it.uuid != group.uuid } + updatedGroup)"
    print "        }"
    print "        _database.value = updatedDb"
    print "        _currentGroup.value = newCurrentGroup"
    print "        // saveDatabase()"
    print "    }"
    print ""
    print $0
    next
}
{ print $0 }
' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt > app/src/main/java/com/example/viewmodel/KeePassViewModel.kt.new
mv app/src/main/java/com/example/viewmodel/KeePassViewModel.kt.new app/src/main/java/com/example/viewmodel/KeePassViewModel.kt
