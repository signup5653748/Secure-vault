package com.example

import app.keemobile.kotpass.constants.BasicField
import app.keemobile.kotpass.models.Entry
import org.junit.Test

class TestKotpass3 {
    @Test
    fun test() {
        val methods = BasicField::class.java.methods
        for (m in methods) {
            println("METHOD: " + m.name)
        }
        val fields = BasicField::class.java.fields
        for (f in fields) {
            println("FIELD: " + f.name)
        }
    }
}
