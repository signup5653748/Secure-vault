package com.example.viewmodel

import app.keemobile.kotpass.models.Group
import java.util.UUID

fun findParent(root: Group, childUuid: UUID): Group? {
    if (root.groups.any { it.uuid == childUuid }) return root
    for (g in root.groups) {
        val p = findParent(g, childUuid)
        if (p != null) return p
    }
    return null
}
