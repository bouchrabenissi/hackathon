import React from "react";
import { View, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { ThemedText } from "./ThemedText";

export function CropHealthStatus() {
  return (
    <View>
      <ThemedText type="subtitle">Crop Health Status</ThemedText>
      <View style={styles.row}>
        <Ionicons
          name="checkmark-circle"
          size={48}
          color="green"
          style={styles.icon}
        />
        <ThemedText style={styles.mediumText}>All Crops Healthy</ThemedText>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  icon: {
    marginRight: 12,
  },
  mediumText: {
    fontSize: 18,
  },
});
