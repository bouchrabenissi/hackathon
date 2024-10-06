"use client";

import { TrendingUp } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  XAxis,
  YAxis,
} from "recharts";

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

// Sample data - replace with your actual data
const precipitationData = [
  { date: "2023-01-01", PRECTOTCORR: 5 },
  { date: "2023-01-02", PRECTOTCORR: 0 },
  { date: "2023-01-03", PRECTOTCORR: 10 },
  { date: "2023-01-04", PRECTOTCORR: 2 },
  { date: "2023-01-05", PRECTOTCORR: 0 },
  { date: "2023-01-06", PRECTOTCORR: 8 },
  { date: "2023-01-07", PRECTOTCORR: 3 },
];

const precipitationDays = precipitationData.filter(
  (day) => day.PRECTOTCORR > 0
).length;

const chartConfig = {
  precipitation: {
    label: "Precipitation",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig;

export function PrecipitationChart() {
  return (
    <Card className="flex flex-col">
      <CardHeader className="text-center">
        <CardTitle>Total Precipitation Frequency</CardTitle>
        <CardDescription>Rainfall in your fields this week</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart
            accessibilityLayer
            data={precipitationData}
            margin={{
              top: 0,
              right: 0,
              left: 0,
              bottom: 0,
            }}>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              tickFormatter={(value) => value.slice(5)} // Show only MM-DD
            />
            <YAxis
              label={{
                value: "Precipitation (mm)",
                angle: -90,
                position: "insideLeft",
                style: { textAnchor: "middle" },
              }}
              tickLine={false}
              axisLine={false}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Bar
              dataKey="PRECTOTCORR"
              fill="var(--color-precipitation)"
              radius={8}>
              <LabelList
                dataKey="PRECTOTCORR"
                position="top"
                offset={12}
                className="fill-foreground"
                fontSize={12}
              />
            </Bar>
          </BarChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm text-center">
        <div className="flex w-full items-center justify-center gap-2 text-sm">
          {precipitationDays} days with rainfall this week{" "}
          <TrendingUp className="h-4 w-4" />
        </div>
        <div className="text-muted-foreground">
          Consider adjusting your irrigation schedule
        </div>
      </CardFooter>
    </Card>
  );
}
