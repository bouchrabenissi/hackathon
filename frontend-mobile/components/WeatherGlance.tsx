import React from "react";
import { View, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "@react-navigation/native";
import { ThemedText } from "./ThemedText";

export function WeatherGlance() {
  const { colors } = useTheme();

  return (
    <View>
      <ThemedText type="subtitle">Weather at a Glance</ThemedText>
      <View style={styles.row}>
        <Ionicons
          name="sunny"
          size={48}
          color={colors.text}
          style={styles.icon}
        />
        <ThemedText style={styles.largeText}>25°C</ThemedText>
      </View>
      <ThemedText style={styles.mediumText}>Rain in 3 hours</ThemedText>
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
  largeText: {
    fontSize: 24,
    fontWeight: "bold",
  },
  mediumText: {
    fontSize: 18,
  },
});
