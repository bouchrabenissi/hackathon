import React from "react";
import { View, StyleSheet } from "react-native";
import { ThemedText } from "./ThemedText";

export function SoilMoisture() {
  return (
    <View>
      <ThemedText type="subtitle">Soil Moisture Level</ThemedText>
      <ThemedText style={styles.mediumText}>Soil Moisture: Good</ThemedText>
      <View style={styles.moistureBar}>
        <View style={styles.moistureLevel} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  mediumText: {
    fontSize: 18,
  },
  moistureBar: {
    height: 20,
    backgroundColor: "#e0e0e0",
    borderRadius: 10,
    marginTop: 8,
  },
  moistureLevel: {
    height: "100%",
    backgroundColor: "green",
    borderRadius: 10,
    width: "70%", // This should be dynamic based on actual moisture level
  },
});
