import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

bad_drag = """                                    .pointerInput(Unit) {
                                        detectDragGesturesAfterLongPress(
                                            onDrag = { change, dragAmount -> 
                                                change.consume()
                                                val threshold = 50f
                                                if (dragAmount.y > threshold && index < fieldOrder.size - 1) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index + 1]
                                                    mutableOrder[index + 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                } else if (dragAmount.y < -threshold && index > 0) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index - 1]
                                                    mutableOrder[index - 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                }
                                            }
                                        )
                                    }"""

good_drag = """                                    .pointerInput(Unit) {
                                        var accumulatedDrag = 0f
                                        detectDragGesturesAfterLongPress(
                                            onDragStart = { accumulatedDrag = 0f },
                                            onDrag = { change, dragAmount -> 
                                                change.consume()
                                                accumulatedDrag += dragAmount.y
                                                val threshold = 150f
                                                if (accumulatedDrag > threshold && index < fieldOrder.size - 1) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index + 1]
                                                    mutableOrder[index + 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                } else if (accumulatedDrag < -threshold && index > 0) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index - 1]
                                                    mutableOrder[index - 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                }
                                            }
                                        )
                                    }"""

text = text.replace(bad_drag, good_drag)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

print("Fixed drag logic")
