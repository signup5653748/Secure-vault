#!/bin/bash
sed -i 's/onNavigateToAddGroup = { navController.navigate("add_group") },/onNavigateToAddGroup = { navController.navigate("add_group") },\n                    onNavigateToEditGroup = { navController.navigate("edit_group") },/g' app/src/main/java/com/example/ui/AppNavigation.kt

sed -i 's/onNavigateToAddEntry = {/onNavigateToEditEntry = { navController.navigate("edit_entry") },\n                    onNavigateToAddEntry = {/g' app/src/main/java/com/example/ui/AppNavigation.kt
