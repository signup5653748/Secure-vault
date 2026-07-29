import re

with open("app/src/main/java/com/example/ui/AppNavigation.kt", "r") as f:
    content = f.read()

# Add templates navigation routes
routes = """        composable("templates") {
            if (database != null) {
                TemplatesScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() },
                    onNavigateToAddTemplate = { navController.navigate("add_template") }
                )
            }
        }
        composable("add_template") {
            if (database != null) {
                AddEntryScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() },
                    isTemplate = true
                )
            }
        }
        composable("settings") {"""

content = content.replace('        composable("settings") {', routes)

# Add onNavigateToTemplates to VaultScreen invocation
content = content.replace("onNavigateToAddEntry = {", "onNavigateToTemplates = { navController.navigate(\"templates\") },\n                    onNavigateToAddEntry = {")

with open("app/src/main/java/com/example/ui/AppNavigation.kt", "w") as f:
    f.write(content)
