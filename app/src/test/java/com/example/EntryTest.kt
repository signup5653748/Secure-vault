package com.example

import org.junit.Test
import app.keemobile.kotpass.models.Entry
import app.keemobile.kotpass.models.EntryFields
import app.keemobile.kotpass.models.EntryValue
import app.keemobile.kotpass.constants.BasicField

class EntryTest {
    @Test
    fun testEntry() {
        val entry = Entry(
            fields = EntryFields(mapOf(
                BasicField.Title() to EntryValue.Plain("Test")
            ))
        )
        println(entry[BasicField.Title]?.content)
        println(entry[BasicField.Notes]?.content)
    }
}
