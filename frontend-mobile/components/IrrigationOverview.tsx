import React from "react";
import { View, StyleSheet, TouchableOpacity } from "react-native";
import { useTheme } from "@react-navigation/native";
import { ThemedText } from "./ThemedText";

export function IrrigationOverview() {
  const { colors } = useTheme();

  return (
    <View>
      <ThemedText type="subtitle">Irrigation Overview</ThemedText>
      <ThemedText style={styles.mediumText}>Water in 2 hours</ThemedText>
      <TouchableOpacity
        style={[styles.button, { backgroundColor: colors.primary }]}
        onPress={() => console.log("Start irrigation")}>
        <ThemedText style={styles.buttonText}>Start Irrigation</ThemedText>
      </TouchableOpacity>
      <ThemedText style={styles.mediumText}>Watering Complete Today</ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  mediumText: {
    fontSize: 18,
  },
  button: {
    padding: 12,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 8,
  },
  buttonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "bold",
  },
});
