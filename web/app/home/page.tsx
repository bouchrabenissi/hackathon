import { cn } from "@/lib/utils";

export default function Home() {
  const farmerName = "John";

  return (
    <main className="flex min-h-screen flex-col items-center p-4 max-w-md mx-auto bg-background text-foreground">
      <h1 className="text-2xl font-bold mb-4">Hey {farmerName}</h1>

      <section className="w-full mb-6">
        <h2 className="text-xl font-semibold mb-2">
          Today&apos;s News on your crops
        </h2>
      </section>

      <section className="w-full mb-6">
        <h2 className="text-xl font-semibold mb-2">Alerts</h2>
        <div className="space-y-4">
          <ColoredAlert
            icon={WindIcon}
            title="Wind Speed"
            message="Moderate to strong wind speed: Check for damage and use windbreaks."
            severity="warning"
          />

          <ColoredAlert
            icon={HumidityIcon}
            title="Humidity"
            message="Moderate humidity: Generally favorable for growth. Maintain regular watering and check soil moisture."
            severity="success"
          />

          <ColoredAlert
            icon={SunIcon}
            title="Solar Radiation"
            message="High radiation: Monitor soil moisture and water crops adequately."
            severity="warning"
          />

          <ColoredAlert
            icon={TemperatureIcon}
            title="Temperature"
            message="High: Increased evaporation. Monitor for water stress and adjust watering."
            severity="warning"
          />
        </div>
      </section>

      <section className="w-full">
        <h2 className="text-xl font-semibold mb-2">Previsions</h2>
        {/* Add prevision content here */}
      </section>
    </main>
  );
}

interface ColoredAlertProps {
  icon: React.FC<React.SVGProps<SVGSVGElement>>;
  title: string;
  message: string;
  severity: "success" | "warning" | "danger";
}

function ColoredAlert({
  icon: Icon,
  title,
  message,
  severity,
}: ColoredAlertProps) {
  const severityClasses = {
    success: "bg-primary/20 border-primary",
    warning: "bg-orange-500/20 border-orange-500",
    danger: "bg-destructive/20 border-destructive",
  };

  const textColors = {
    success: "text-primary",
    warning: "text-orange-700 dark:text-orange-300",
    danger: "text-destructive",
  };

  return (
    <div
      className={cn(
        severityClasses[severity],
        "border rounded-lg p-4 flex items-start"
      )}>
      <div className="flex-shrink-0 mr-4">
        <Icon className={cn("h-6 w-6", textColors[severity])} />
      </div>
      <div>
        <h3 className={cn("font-semibold leading-6", textColors[severity])}>
          {title}
        </h3>
        <p className="text-foreground/80 mt-1">{message}</p>
      </div>
    </div>
  );
}

const SunIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg
    width="100%"
    height="100%"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    {...props}>
    <path fill="currentColor" d="M18 12a6 6 0 1 1-12 0a6 6 0 0 1 12 0" />
    <path
      fill="currentColor"
      fillRule="evenodd"
      d="M12 1.25a.75.75 0 0 1 .75.75v1a.75.75 0 0 1-1.5 0V2a.75.75 0 0 1 .75-.75M1.25 12a.75.75 0 0 1 .75-.75h1a.75.75 0 0 1 0 1.5H2a.75.75 0 0 1-.75-.75m19 0a.75.75 0 0 1 .75-.75h1a.75.75 0 0 1 0 1.5h-1a.75.75 0 0 1-.75-.75M12 20.25a.75.75 0 0 1 .75.75v1a.75.75 0 0 1-1.5 0v-1a.75.75 0 0 1 .75-.75"
      clipRule="evenodd"
    />
    <path
      fill="currentColor"
      d="M4.398 4.398a.75.75 0 0 1 1.061 0l.393.393a.75.75 0 0 1-1.06 1.06l-.394-.392a.75.75 0 0 1 0-1.06m15.202 0a.75.75 0 0 1 0 1.06l-.392.393a.75.75 0 0 1-1.06-1.06l.392-.393a.75.75 0 0 1 1.06 0m-1.453 13.748a.75.75 0 0 1 1.061 0l.393.393a.75.75 0 0 1-1.06 1.06l-.394-.392a.75.75 0 0 1 0-1.06m-12.295 0a.75.75 0 0 1 0 1.06l-.393.393a.75.75 0 1 1-1.06-1.06l.392-.393a.75.75 0 0 1 1.06 0"
      opacity=".5"
    />
  </svg>
);

const WindIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg
    width="100%"
    height="100%"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    {...props}>
    <g
      fill="none"
      stroke="currentColor"
      strokeLinecap="round"
      strokeWidth="1.5">
      <path d="M3 8h6.5A2.5 2.5 0 1 0 7 5.5v.357M4 14h14.5a3.5 3.5 0 1 1-3.5 3.5V17" />
      <path d="M2 11h16.5A3.5 3.5 0 1 0 15 7.5V8" opacity=".5" />
    </g>
  </svg>
);

const HumidityIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg
    width="100%"
    height="100%"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    {...props}>
    <g
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      transform="scale(1.1) translate(-1.2, -1.2)">
      <path
        strokeLinecap="round"
        d="M6.286 19C3.919 19 2 17.104 2 14.765s1.919-4.236 4.286-4.236q.427.001.83.08m7.265-2.582a5.8 5.8 0 0 1 1.905-.321c.654 0 1.283.109 1.87.309m-11.04 2.594a5.6 5.6 0 0 1-.354-1.962C6.762 5.528 9.32 3 12.476 3c2.94 0 5.361 2.194 5.68 5.015m-11.04 2.594a4.3 4.3 0 0 1 1.55.634m9.49-3.228C20.392 8.78 22 10.881 22 13.353c0 2.707-1.927 4.97-4.5 5.52"
        opacity=".5"
      />
      <path d="M15 19.084C15 20.694 13.657 22 12 22s-3-1.305-3-2.916c0-.912.961-2.1 1.796-2.96a1.665 1.665 0 0 1 2.408 0c.835.86 1.796 2.048 1.796 2.96Z" />
    </g>
  </svg>
);

const TemperatureIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg
    width="100%"
    height="100%"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    {...props}>
    <g transform="scale(1.1) translate(-1.2, -1.2)">
      <path
        fill="currentColor"
        d="M17.5 16.5a5.5 5.5 0 1 1-8.939-4.293c.264-.211.439-.521.439-.86V5a3 3 0 1 1 6 0v6.348c0 .338.175.648.439.86A5.49 5.49 0 0 1 17.5 16.5"
        opacity=".5"
      />
      <path
        fill="currentColor"
        d="M12.75 5a.75.75 0 0 0-1.5 0v8.38c0 .437-.297.808-.658 1.054a2.5 2.5 0 1 0 2.816 0c-.36-.246-.658-.617-.658-1.054z"
      />
    </g>
  </svg>
);
