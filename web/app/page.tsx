"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function InitialPage() {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Store name in local storage
    localStorage.setItem("farmerName", name);

    try {
      const response = await fetch("/api/py/get_lat_lon", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ location }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store lat and lon in local storage
        localStorage.setItem("farmerLat", data.lat);
        localStorage.setItem("farmerLon", data.lon);
        // Redirect to home page
        router.push("/home");
      } else {
        console.error("Failed to get lat/lon");
        // You might want to show an error message to the user here
      }
    } catch (error) {
      console.error("Error:", error);
      // You might want to show an error message to the user here
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen">
      <Image
        src="/images/male-farmer.webp"
        alt="Male farmer"
        width={175}
        height={175}
        className="absolute bottom-24 left-0"
      />
      <Image
        src="/images/female-farmer.webp"
        alt="Female farmer"
        width={175}
        height={175}
        className="absolute bottom-24 right-0"
      />

      <main className="flex min-h-screen flex-col items-center justify-center p-4 max-w-md mx-auto bg-background text-foreground">
        <h1 className="text-3xl font-bold mb-2">Welcome to Crop IT</h1>
        <p className="text-center text-muted-foreground mb-6">
          Your personal assistant for smart and sustainable farming
        </p>
        <form onSubmit={handleSubmit} className="w-full space-y-4">
          <div>
            <label htmlFor="name" className="block mb-2">
              Name:
            </label>
            <Input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
              required
            />
          </div>
          <div>
            <label htmlFor="location" className="block mb-2">
              Location:
            </label>
            <Input
              type="text"
              id="location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Enter your location"
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Loading..." : "Get Started"}
          </Button>
        </form>
      </main>
    </div>
  );
}
