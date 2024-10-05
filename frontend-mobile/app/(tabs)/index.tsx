import React from "react";
import { StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useTheme } from "@react-navigation/native";
import { ThemedView } from "@/components/ThemedView";
import { WeatherGlance } from "@/components/WeatherGlance";
import { SoilMoisture } from "@/components/SoilMoisture";
import { IrrigationOverview } from "@/components/IrrigationOverview";
import { CropHealthStatus } from "@/components/CropHealthStatus";

export default function HomeScreen() {
  const { colors } = useTheme();

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      padding: 16,
    },
    section: {
      marginBottom: 24,
      backgroundColor: colors.card,
      borderRadius: 12,
      padding: 16,
    },
  });

  return (
    <SafeAreaView style={styles.container}>
      <ThemedView style={styles.section}>
        <WeatherGlance />
      </ThemedView>

      <ThemedView style={styles.section}>
        <SoilMoisture />
      </ThemedView>

      <ThemedView style={styles.section}>
        <IrrigationOverview />
      </ThemedView>

      <ThemedView style={styles.section}>
        <CropHealthStatus />
      </ThemedView>
    </SafeAreaView>
  );
}
