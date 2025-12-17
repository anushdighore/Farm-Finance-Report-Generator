document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("financeForm");
  let validatedPayload = null; // Store validated data for PDF generation

  // Form Submit
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Collect Farmer & Crop Details
    const farmerDetails = {
      farmer_name: document.getElementById("farmerName").value,
      crop_name: document.getElementById("cropName").value,
      season: document.getElementById("season").value,
      total_acres: parseFloat(document.getElementById("totalAcres").value),
      sowing_date: document.getElementById("sowingDate").value,
      harvest_date: document.getElementById("harvestDate").value,
      village: document.getElementById("village").value,
      taluka: document.getElementById("taluka").value,
      district: document.getElementById("district").value,
      state: document.getElementById("state").value,
    };

    // Collect All Expenses (only rows with values)
    const expenses = Array.from(document.querySelectorAll(".expense-item"))
      .map((item) => {
        const category = item.querySelector(".expense-category").value;
        const amount = item.querySelector(".expense-amount").value;
        const expense_date = item.querySelector(".expense-date").value;
        const description = item.querySelector(".expense-description").value;

        // Only include if category is not empty, otherwise set amount to 0
        if (category) {
          return {
            category: category,
            amount: amount ? parseFloat(amount) : 0,
            expense_date: expense_date || null,
            description: description || null,
          };
        }
      })
      .filter((item) => item !== undefined);

    // Collect All Income (only rows with values)
    const income = Array.from(document.querySelectorAll(".income-item"))
      .map((item) => {
        const category = item.querySelector(".income-category").value;
        const amount = item.querySelector(".income-amount").value;
        const income_date = item.querySelector(".income-date").value;
        const description = item.querySelector(".income-description").value;

        // Only include if category is not empty, otherwise set amount to 0
        if (category) {
          return {
            category: category,
            amount: amount ? parseFloat(amount) : 0,
            income_date: income_date || null,
            description: description || null,
          };
        }
      })
      .filter((item) => item !== undefined);

    // Check if at least one expense and income entry
    if (expenses.length === 0 || income.length === 0) {
      alert("❌ Please fill at least one expense and one income entry");
      return;
    }

    const payload = {
      farmer_details: farmerDetails,
      expenses: expenses,
      income: income,
    };

    console.log("📤 Submitting payload:", payload);

    try {
      const response = await fetch("/api/validate-finance", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      console.log("📥 Response status:", response.status);
      const result = await response.json();
      console.log("📥 Response body:", result);

      if (response.ok) {
        // Store validated payload for PDF generation
        validatedPayload = payload;

        // Show Summary
        document.getElementById("totalExpenses").textContent =
          result.total_expenses.toFixed(2);
        document.getElementById("totalIncome").textContent =
          result.total_income.toFixed(2);
        document.getElementById("netProfit").textContent =
          result.net_profit.toFixed(2);
        document.getElementById("summaryBox").style.display = "block";

        // Show PDF download button
        document.getElementById("downloadPdfBtn").style.display =
          "inline-block";

        // alert(
        //   "✅ Finance data validated successfully! You can now download the PDF report."
        // );
      } else {
        // Format validation errors for better readability
        const errorMsg = Array.isArray(result.detail)
          ? result.detail
              .map((e) => `${e.loc?.join(" → ") || "Field"}: ${e.msg}`)
              .join("\n")
          : result.detail || "Unknown error";

        console.error("❌ Server validation errors:", result.detail);
        alert("❌ Validation Error:\n\n" + errorMsg);
      }
    } catch (error) {
      console.error("❌ Request failed:", error);
      alert("❌ Error submitting form: " + error);
    }
  });

  // PDF Download Handler
  const downloadPdfBtn = document.getElementById("downloadPdfBtn");
  if (downloadPdfBtn) {
    downloadPdfBtn.addEventListener("click", async function () {
      if (!validatedPayload) {
        alert("❌ Please validate the finance data first!");
        return;
      }

      console.log("📄 Generating PDF...");

      try {
        const response = await fetch("/api/generate-report", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(validatedPayload),
        });

        if (response.ok) {
          // Get filename from Content-Disposition header
          const contentDisposition = response.headers.get(
            "Content-Disposition"
          );
          let filename = "Finance_Report.pdf";
          if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename=(.+)/);
            if (filenameMatch) {
              filename = filenameMatch[1];
            }
          }

          // Download the PDF
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);

          console.log("✅ PDF downloaded successfully:", filename);
          // alert("✅ PDF report downloaded successfully!");
        } else {
          const error = await response.json();
          console.error("❌ PDF generation failed:", error);
          alert(
            "❌ Failed to generate PDF: " + (error.detail || "Unknown error")
          );
        }
      } catch (error) {
        console.error("❌ PDF download error:", error);
        alert("❌ Error downloading PDF: " + error);
      }
    });
  }
});
