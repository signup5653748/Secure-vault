package com.example

import app.keemobile.kotpass.constants.BasicField
import org.junit.Test
import kotlin.reflect.full.*

class TestKotpass4 {
    @Test
    fun test() {
        val t = BasicField.Title
        println("TYPE IS: ${t::class.java.name}")
    }
}
