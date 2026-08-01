package com.example.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.viewmodel.KeePassViewModel

@Composable
fun AppNavigation(viewModel: KeePassViewModel) {
    val navController = rememberNavController()
    val database by viewModel.database.collectAsState()

    NavHost(navController = navController, startDestination = "auth") {
        composable("auth") {
            LaunchedEffect(database) {
                if (database != null) {
                    navController.navigate("secure") {
                        popUpTo("auth") { inclusive = true }
                    }
                }
            }
            if (database == null) {
                AuthScreen(
                    viewModel = viewModel,
                    onNavigateToCreate = { navController.navigate("create_database") }
                )
            }
        }
        composable("create_database") {
            CreateDatabaseScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable("secure") {
            LaunchedEffect(database) {
                if (database == null) {
                    navController.navigate("auth") {
                        popUpTo("secure") { inclusive = true }
                    }
                }
            }
            if (database != null) {
                SecureScreen(
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
                    onNavigateToTemplates = { navController.navigate("templates") },
                    onNavigateToAddTemplate = { navController.navigate("add_template") },
                    onNavigateToAddNote = { navController.navigate("add_note") },
                    onNavigateToAddGroup = { navController.navigate("add_group") },
                    onNavigateToEditGroup = { navController.navigate("edit_group") },
                    onNavigateToEditEntry = { navController.navigate("edit_entry") },
                    onNavigateToAddEntry = {
                        navController.navigate("add_entry")
                    }
                )
            }
        }
        composable("add_group") {
            if (database != null) {
                AddGroupScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() }
                )
            }
        }
        composable("edit_group") {
            if (database != null) {
                AddGroupScreen(
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
        composable("view") {
            if (database != null) {
                ViewEntryScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() },
                    onNavigateToEdit = { navController.navigate("edit_entry") }
                )
            } else {
                LaunchedEffect(Unit) {
                    navController.navigate("auth") {
                        popUpTo(0)
                    }
                }
            }
        }
        composable("add_note") {
            if (database != null) {
                AddNoteScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() }
                )
            }
        }
                composable("edit_entry") {
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
        composable("add_entry") {
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
        }
        composable("templates") {
            if (database != null) {
                TemplatesScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() },
                    onNavigateToAddTemplate = { navController.navigate("add_template") },
                    onNavigateToEditTemplate = { navController.navigate("edit_template") }
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
        composable("edit_template") {
            if (database != null) {
                AddEntryScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() },
                    isTemplate = true,
                    isEdit = true
                )
            }
        }
        composable("settings") {
            SettingsScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable("about") {
            AboutScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
