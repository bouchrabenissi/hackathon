"use client";

import { TrendingUp } from "lucide-react";
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts";

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

export const description = "Relative Humidity Over Time";

const chartData = [
  { date: "2024-01-01", humidity: 65 },
  { date: "2024-01-02", humidity: 70 },
  { date: "2024-01-03", humidity: 68 },
  { date: "2024-01-04", humidity: 72 },
  { date: "2024-01-05", humidity: 75 },
  { date: "2024-01-06", humidity: 71 },
  // Add more data points as needed
];

const chartConfig = {
  humidity: {
    label: "Humidity",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig;

export function HumidityChart() {
  return (
    <Card>
      <CardHeader className="text-center">
        <CardTitle>Relative Humidity Over Time</CardTitle>
        <CardDescription>
          Moisture levels in your fields this week
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <AreaChart
            accessibilityLayer
            data={chartData}
            margin={{
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
            }}>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickFormatter={(value) => new Date(value).toLocaleDateString()}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tickMargin={0}
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent indicator="line" />}
            />
            <Area
              dataKey="humidity"
              type="natural"
              fill="var(--color-humidity)"
              fillOpacity={0.4}
              stroke="var(--color-humidity)"
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="text-center">
        <div className="flex w-full flex-col items-center gap-2 text-sm">
          <div className="flex items-center gap-2 font-medium leading-none">
            Average humidity: 70.2% <TrendingUp className="h-4 w-4" />
          </div>
          <div className="text-muted-foreground">
            Good moisture levels for most crops
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
