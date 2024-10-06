import { PrecipitationChart } from "@/components/precipitation-chart";
import { TemperatureChart } from "@/components/temperature-chart";
import { HumidityChart } from "@/components/humidity-chart";
import { AllChart } from "@/components/all-charts";

export default function ChartsPage() {
  return (
    <div className="flex flex-col gap-4 p-4">
      <PrecipitationChart />
      <TemperatureChart />
      <HumidityChart />
      <AllChart />
    </div>
  );
}
