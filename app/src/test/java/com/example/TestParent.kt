package com.example

import app.keemobile.kotpass.database.KeePassDatabase
import app.keemobile.kotpass.models.Group
import org.junit.Test
import java.util.UUID

class TestParent {
    @Test
    fun test() {
        println(KeePassDatabase::class.java.methods.joinToString("\n") { it.name })
        println("Group methods:")
        println(Group::class.java.methods.joinToString("\n") { it.name })
    }
}
