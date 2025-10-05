document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("runBtn");
  
    button.addEventListener("click", async () => {
      const name = document.getElementById("nameInput").value;
  
      // Send data to Python backend
      const response = await fetch("http://127.0.0.1:5000/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: name })
      });
  
      const result = await response.json();
      console.log("Response from Python:", result.message);
    });
  });
  