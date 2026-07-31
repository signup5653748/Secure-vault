package com.example

import app.keemobile.kotpass.database.KeePassDatabase
import app.keemobile.kotpass.models.Group
import org.junit.Test

class TestKotpassParent {
    @Test
    fun test() {
        val root = Group(name = "Root")
        val child = Group(name = "Child")
        val dbRoot = root.copy(groups = listOf(child))
        println("TYPE IS: ${dbRoot.javaClass.name}")
    }
}
