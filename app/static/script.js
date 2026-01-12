async function planTrip() {
  const destination = document.getElementById("destination").value;
  const days = document.getElementById("days").value;
  const people = document.getElementById("people").value;
  const budget = document.getElementById("budget").value;

  // Basic validation
  if (!destination || !days || !people) {
    alert("Please fill destination, days, and number of travelers");
    return;
  }

  // Show loading, reset output and export buttons
  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("output").textContent = "";
  document.getElementById("exportButtons").classList.add("hidden");

  try {
    const response = await fetch("/plan-trip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        destination: destination,
        days: parseInt(days),
        people: parseInt(people),
        budget: budget
      })
    });

    const data = await response.json();

    // Hide loading
    document.getElementById("loading").classList.add("hidden");

    // Show output
    document.getElementById("output").textContent =
      data.itinerary || "No itinerary received.";

    // Show export buttons ONLY if itinerary exists
    if (data.itinerary) {
      document.getElementById("exportButtons").classList.remove("hidden");
    }

  } catch (error) {
    document.getElementById("loading").classList.add("hidden");
    alert("Something went wrong while generating the trip. Please try again.");
    console.error(error);
  }
}
