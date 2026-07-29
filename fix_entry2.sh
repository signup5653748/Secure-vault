#!/bin/bash
sed -i '/item { Spacer(modifier = Modifier.height(8.dp)) }/a \
            item {\n\
                Row(\n\
                    modifier = Modifier.fillMaxWidth(),\n\
                    horizontalArrangement = Arrangement.Center,\n\
                    verticalAlignment = Alignment.CenterVertically\n\
                ) {\n\
                    Spacer(modifier = Modifier.width(48.dp))\n\
                    Box(\n\
                        modifier = Modifier\n\
                            .size(80.dp)\n\
                            .background(Color.Transparent, CircleShape)\n\
                            .androidx.compose.foundation.border(2.dp, parseColor(color), CircleShape)\n\
                            .clickable { showIconDialog = true },\n\
                        contentAlignment = Alignment.Center\n\
                    ) {\n\
                        val iconColor = parseColor(color)\n\
                        val iconVector = parseIcon(iconName)\n\
                        Icon(iconVector, contentDescription = "Select Icon", tint = iconColor, modifier = Modifier.size(40.dp))\n\
                    }\n\
                    Spacer(modifier = Modifier.width(16.dp))\n\
                    IconButton(onClick = { showColorDialog = true }) {\n\
                        Icon(Icons.Default.Palette, contentDescription = "Select Color", tint = parseColor(color))\n\
                    }\n\
                }\n\
            }' app/src/main/java/com/example/ui/AddEntryScreen.kt
