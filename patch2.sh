#!/bin/bash
awk '
/composable\("add_group"\) \{/ {
    print $0
    in_add_group = 1
    brace_count = 1
    next
}
in_add_group {
    print $0
    if ($0 ~ /\{/) brace_count++
    if ($0 ~ /\}/) brace_count--
    if (brace_count == 0) {
        in_add_group = 0
        print "        composable(\"edit_group\") {"
        print "            if (database != null) {"
        print "                AddGroupScreen("
        print "                    viewModel = viewModel,"
        print "                    onNavigateBack = { navController.popBackStack() },"
        print "                    isEdit = true"
        print "                )"
        print "            } else {"
        print "                LaunchedEffect(Unit) {"
        print "                    navController.navigate(\"auth\") {"
        print "                        popUpTo(0)"
        print "                    }"
        print "                }"
        print "            }"
        print "        }"
    }
    next
}
{ print $0 }
' app/src/main/java/com/example/ui/AppNavigation.kt > app/src/main/java/com/example/ui/AppNavigation.kt.new
mv app/src/main/java/com/example/ui/AppNavigation.kt.new app/src/main/java/com/example/ui/AppNavigation.kt
