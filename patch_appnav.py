import re

with open('/app/applet/app/src/main/java/com/example/ui/AppNavigation.kt', 'r') as f:
    content = f.read()

view_old = """        composable("view") {
            if (database != null) {
                ViewEntryScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() }
                )
            } else {"""
view_new = """        composable("view") {
            if (database != null) {
                ViewEntryScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() },
                    onNavigateToEdit = { navController.navigate("edit_entry") }
                )
            } else {"""
content = content.replace(view_old, view_new)

edit_route = """        composable("edit_entry") {
            if (database != null) {
                AddEntryScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() },
                    isEdit = true
                )
            } else {
                LaunchedEffect(Unit) {
                    navController.navigate("auth") {
                        popUpTo(0)
                    }
                }
            }
        }
"""
if 'composable("edit_entry")' not in content:
    content = content.replace('composable("add_entry") {', edit_route + '        composable("add_entry") {')

with open('/app/applet/app/src/main/java/com/example/ui/AppNavigation.kt', 'w') as f:
    f.write(content)
