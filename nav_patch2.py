import re

with open("app/src/main/java/com/example/ui/AppNavigation.kt", "r") as f:
    content = f.read()

# Add add_note navigation route
routes = """        composable("add_note") {
            if (database != null) {
                AddNoteScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() }
                )
            }
        }
        composable("add_entry") {"""

content = content.replace('        composable("add_entry") {', routes)

# Add onNavigateToAddNote to VaultScreen invocation
content = content.replace("onNavigateToAddEntry = {", "onNavigateToAddNote = { navController.navigate(\"add_note\") },\n                    onNavigateToAddEntry = {")

with open("app/src/main/java/com/example/ui/AppNavigation.kt", "w") as f:
    f.write(content)
