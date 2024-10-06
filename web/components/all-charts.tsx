"use client";

import { TrendingUp } from "lucide-react";
import { PolarAngleAxis, PolarGrid, Radar, RadarChart } from "recharts";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

export const description = "Your field's weather conditions";

const chartData = [
  { parameter: "Temperature", value: 25 },
  { parameter: "Wind Speed", value: 15 },
  { parameter: "Humidity", value: 60 },
  { parameter: "Precipitation", value: 30 },
  { parameter: "Solar Radiation", value: 70 },
];

const chartConfig = {
  weatherConditions: {
    label: "Weather Conditions",
    color: "hsl(var(--chart-1))",
  },
} satisfies ChartConfig;

export function AllChart() {
  return (
    <Card>
      <CardHeader className="text-center">
        <CardTitle>Weather Conditions Overview</CardTitle>
        <CardDescription>
          Key factors affecting your crop management
        </CardDescription>
      </CardHeader>
      <CardContent className="pb-0">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square max-h-[250px]">
          <RadarChart data={chartData}>
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <PolarAngleAxis dataKey="parameter" />
            <PolarGrid />
            <Radar
              dataKey="value"
              name="Weather Conditions"
              fill="var(--color-weatherConditions)"
              fillOpacity={0.6}
              dot={{
                r: 4,
                fillOpacity: 1,
              }}
            />
          </RadarChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm text-center">
        <div className="flex justify-center items-center gap-2 font-medium leading-none">
          Weather conditions in your fields <TrendingUp className="h-4 w-4" />
        </div>
        <div className="text-muted-foreground">
          Overview to guide your planting, irrigation, and crop protection
          decisions
        </div>
      </CardFooter>
    </Card>
  );
}
