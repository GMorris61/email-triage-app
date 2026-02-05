// -----------------------------
// CONFIG
// -----------------------------
const API_BASE_URL = "http://email-backend-service:8080";


// -----------------------------
// SEARCH EMAILS
// -----------------------------
async function searchEmails() {
  const keyword = document.getElementById("keywordInput").value.trim();
  const statusMessage = document.getElementById("statusMessage");

  if (!keyword) {
    statusMessage.textContent = "Please enter a keyword before searching.";
    return;
  }

  statusMessage.textContent = "Searching...";

  try {
    const response = await fetch(
      `${API_BASE_URL}/email/search?keyword=${encodeURIComponent(keyword)}`
    );

    if (!response.ok) {
      throw new Error("Backend returned an error");
    }

    const data = await response.json();

    // Save results to localStorage so results.html can access them
    localStorage.setItem("searchResults", JSON.stringify(data));

    // Navigate to results page
    window.location.href = "results.html";

  } catch (error) {
    statusMessage.textContent = "Error searching emails. Please try again.";
    console.error("Search error:", error);
  }
}


// -----------------------------
// LOAD RESULTS ON RESULTS PAGE
// -----------------------------
function loadResults() {
  const resultsContainer = document.getElementById("resultsContainer");
  const rawData = localStorage.getItem("searchResults");

  if (!rawData) {
    resultsContainer.innerHTML = "<p>No results found or search not performed.</p>";
    return;
  }

  const data = JSON.parse(rawData);

  if (!data.results || data.results.length === 0) {
    resultsContainer.innerHTML = "<p>No emails matched your search.</p>";
    return;
  }

  // Build results list
  let html = `<h2>Results for "${data.keyword}"</h2>`;
  html += `<ul class="email-list">`;

  data.results.forEach(email => {
    html += `
  <li id="email-${email.id}">
    <strong>From:</strong> ${email.sender}<br>
    <strong>Subject:</strong> ${email.subject}<br>
    <button onclick="performAction('${email.id}', 'trash')">Trash</button>
    <button onclick="performAction('${email.id}', 'archive')">Archive</button>
    <button onclick="performAction('${email.id}', 'dry-run')">Dry Run</button>
  </li>
`;

  });

  html += `</ul>`;
  resultsContainer.innerHTML = html;
}


// -----------------------------
// PERFORM ACTION (Trash, Archive, Dry-run)
// -----------------------------
async function performAction(emailId, action) {
  const actionMessage = document.getElementById("actionMessage");
  actionMessage.textContent = `Performing ${action}...`;

  try {
    const response = await fetch(`${API_BASE_URL}/email/action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email_ids: [emailId],
        action: action
      })
    });

    if (!response.ok) {
      throw new Error("Backend returned an error");
    }

    const data = await response.json();
    actionMessage.textContent = data.result;

    // ⭐ Remove the email from the page
    const emailElement = document.getElementById(`email-${emailId}`);
    if (emailElement) {
      emailElement.remove();
    }

  } catch (error) {
    actionMessage.textContent = "Error performing action.";
    console.error("Action error:", error);
  }
}
