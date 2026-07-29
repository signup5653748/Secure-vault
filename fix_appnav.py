import re

with open("app/src/main/java/com/example/ui/AppNavigation.kt", "r") as f:
    content = f.read()

# Add onNavigateToAddEntry to VaultScreen
vault_call = """                VaultScreen(
                    viewModel = viewModel, 
                    onNavigateToView = {
                        navController.navigate("view")
                    },
                    onNavigateToSettings = {
                        navController.navigate("settings")
                    },
                    onNavigateToCreate = {
                        navController.navigate("create_database")
                    },
                    onNavigateToAbout = {
                        navController.navigate("about")
                    }
                )"""

new_vault_call = """                VaultScreen(
                    viewModel = viewModel, 
                    onNavigateToView = {
                        navController.navigate("view")
                    },
                    onNavigateToSettings = {
                        navController.navigate("settings")
                    },
                    onNavigateToCreate = {
                        navController.navigate("create_database")
                    },
                    onNavigateToAbout = {
                        navController.navigate("about")
                    },
                    onNavigateToAddEntry = {
                        navController.navigate("add_entry")
                    }
                )"""
content = content.replace(vault_call, new_vault_call)

add_entry_screen = """        composable("add_entry") {
            if (database != null) {
                AddEntryScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() }
                )
            } else {
                LaunchedEffect(Unit) {
                    navController.navigate("auth") {
                        popUpTo(0)
                    }
                }
            }
        }"""
content = content.replace('        composable("settings")', add_entry_screen + '\n        composable("settings")')

with open("app/src/main/java/com/example/ui/AppNavigation.kt", "w") as f:
    f.write(content)

