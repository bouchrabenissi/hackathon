"use client";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function App() {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [response, setResponse] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/py/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, location }),
      });
      const data = await res.json();
      if (res.ok) {
        // If the request was successful, store the response in localStorage
        localStorage.setItem("cropCareResponse", data.message);
        // Redirect to the home page
        router.push("/home");
      } else {
        setResponse("An error occurred while submitting the form.");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      setResponse("An error occurred while submitting the form.");
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 max-w-md mx-auto bg-background text-foreground">
      <h1 className="text-3xl font-bold mb-4">Welcome to CropCare</h1>
      <p className="text-center mb-6">
        We&apos;re here to help you take better care of your crops using
        advanced data from NASA. Our system provides personalized
        recommendations based on your location and current weather conditions.
      </p>
      <form className="w-full space-y-4" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name" className="block text-sm font-medium mb-1">
            Your Name
          </label>
          <Input
            id="name"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="location" className="block text-sm font-medium mb-1">
            Your Location
          </label>
          <Input
            id="location"
            placeholder="Enter your location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>
        <Button type="submit" className="w-full">
          Get Your Recommendations
        </Button>
      </form>
      {response && (
        <div className="mt-4 p-4 bg-gray-100 rounded-md">
          <p className="text-sm">{response}</p>
        </div>
      )}
    </main>
  );
}
