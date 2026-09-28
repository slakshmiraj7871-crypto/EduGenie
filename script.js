/**
 * EduGenie: Interactive Client-side Script
 * Handles UI tab switching, API integration, interactive quiz scoring, and markdown formatting.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const taskSelect = document.getElementById("taskSelect");
  const tabsNav = document.getElementById("tabsNav");
  const eduForm = document.getElementById("eduForm");
  const userInput = document.getElementById("userInput");
  const inputLabel = document.getElementById("inputLabel");
  const charCount = document.getElementById("charCount");
  const starterChips = document.getElementById("starterChips");
  const clearBtn = document.getElementById("clearBtn");
  const submitBtn = document.getElementById("submitBtn");
  const loadingIndicator = document.getElementById("loadingIndicator");
  const loadingMessage = document.getElementById("loadingMessage");
  const resultContainer = document.getElementById("resultContainer");
  const resultModuleBadge = document.getElementById("resultModuleBadge");
  const resultTitle = document.getElementById("resultTitle");
  const resultText = document.getElementById("resultText");
  const copyBtn = document.getElementById("copyBtn");
  const quizDeck = document.getElementById("quizDeck");
  const quizQuestionsContainer = document.getElementById("quizQuestionsContainer");
  const scoreText = document.getElementById("scoreText");
  const scoreProgress = document.getElementById("scoreProgress");

  // Task Configurations
  const TASK_CONFIGS = {
    explain: {
      label: "Concept to Explain:",
      placeholder: "e.g., The Pythagoras Theorem, Photosynthesis, Black Holes, DNA Replication...",
      endpoint: "/explain",
      badge: "Explanation",
      loading: "EduGenie is breaking down this concept into simple terms...",
      starters: [
        "The Pythagoras Theorem",
        "Photosynthesis in Plants",
        "Black Holes & Event Horizons",
        "Newton's Third Law"
      ]
    },
    qa: {
      label: "Your Question:",
      placeholder: "e.g., Which is the largest ocean? Why is the sky blue? How do airplanes generate lift?",
      endpoint: "/qa",
      badge: "Academic Q&A",
      loading: "EduGenie is researching and generating a concise answer...",
      starters: [
        "Which is the largest ocean?",
        "Why is the sky blue?",
        "What causes solar eclipses?",
        "What is the difference between DNA and RNA?"
      ]
    },
    quiz: {
      label: "Passage or Topic for Quiz:",
      placeholder: "e.g., Paste a paragraph about the Solar System or enter 'Renewable Energy' to generate 3 MCQs...",
      endpoint: "/quiz",
      badge: "Quiz Generator",
      loading: "EduGenie is generating 3 multiple-choice questions with 4 options each...",
      starters: [
        "The Solar System and Planets",
        "Renewable vs Non-Renewable Energy",
        "World War II Causes and Alliances",
        "Photosynthesis and Cellular Respiration"
      ]
    },
    summarize: {
      label: "Educational Passage to Summarize:",
      placeholder: "Paste an article, study guide, or textbook chapter here for a high-yield revision summary...",
      endpoint: "/summarize",
      badge: "Summarizer",
      loading: "EduGenie is extracting core concepts and high-yield points...",
      starters: [
        "The Water Cycle and Atmospheric Precipitation",
        "Plate Tectonics and Continental Drift",
        "The Industrial Revolution Impact"
      ]
    },
    recommend: {
      label: "Skill or Topic for Learning Path:",
      placeholder: "e.g., SQL for Data Science, Full-Stack Web Development, Machine Learning from scratch...",
      endpoint: "/learn/recommendations",
      badge: "Learning Path",
      loading: "EduGenie is structuring a beginner-to-advanced roadmap with curated resources...",
      starters: [
        "SQL for Data Science",
        "Python for Beginners",
        "Machine Learning with PyTorch",
        "Web Development with FastAPI & React"
      ]
    }
  };

  let currentTask = "explain";
  let quizState = {
    total: 3,
    answered: 0,
    correctCount: 0
  };

  // Switch Task Mode
  function setTask(taskKey) {
    if (!TASK_CONFIGS[taskKey]) return;
    currentTask = taskKey;

    // Sync Dropdown
    taskSelect.value = taskKey;

    // Sync Tabs
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-task") === taskKey);
    });

    // Update Input UI
    const cfg = TASK_CONFIGS[taskKey];
    inputLabel.textContent = cfg.label;
    userInput.placeholder = cfg.placeholder;

    // Update Starter Chips
    renderStarterChips(cfg.starters);
  }

  // Render Starter Chips
  function renderStarterChips(starters) {
    starterChips.innerHTML = "";
    starters.forEach(text => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "chip-btn";
      chip.textContent = text;
      chip.addEventListener("click", () => {
        userInput.value = text;
        updateCharCount();
        userInput.focus();
      });
      starterChips.appendChild(chip);
    });
  }

  // Character Counter
  function updateCharCount() {
    const len = userInput.value.length;
    charCount.textContent = `${len} character${len === 1 ? "" : "s"}`;
  }

  userInput.addEventListener("input", updateCharCount);

  // Tab click events
  tabsNav.addEventListener("click", (e) => {
    const btn = e.target.closest(".tab-btn");
    if (btn) {
      const task = btn.getAttribute("data-task");
      setTask(task);
    }
  });

  // Dropdown change event
  taskSelect.addEventListener("change", (e) => {
    setTask(e.target.value);
  });

  // Clear Button
  clearBtn.addEventListener("click", () => {
    userInput.value = "";
    updateCharCount();
    userInput.focus();
  });

  // Keyboard shortcut: Ctrl + Enter
  userInput.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      eduForm.dispatchEvent(new Event("submit"));
    }
  });

  // Simple Markdown Renderer
  function renderMarkdown(md) {
    if (!md) return "";
    let html = md
      // Escape HTML entities
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      // Headers
      .replace(/^### (.*$)/gim, "<h3>$1</h3>")
      .replace(/^## (.*$)/gim, "<h2>$1</h2>")
      .replace(/^# (.*$)/gim, "<h1>$1</h1>")
      // Bold
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      // Italic
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      // Code blocks
      .replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
      // Inline code
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      // Blockquotes
      .replace(/^\> (.*$)/gim, "<blockquote>$1</blockquote>")
      // Unordered lists
      .replace(/^\s*[-*]\s+(.*$)/gim, "<li>$1</li>")
      // Ordered lists
      .replace(/^\s*\d+\.\s+(.*$)/gim, "<li>$1</li>")
      // Paragraphs
      .replace(/\n\s*\n/g, "</p><p>")
      .replace(/\n/g, "<br>");

    // Wrap list items with <ul>
    html = html.replace(/(<li>.*<\/li>)/gis, "<ul>$1</ul>");
    return `<p>${html}</p>`;
  }

  // Handle Form Submission
  eduForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const promptText = userInput.value.trim();
    if (!promptText) {
      alert("Please enter some text or select an example prompt!");
      return;
    }

    const cfg = TASK_CONFIGS[currentTask];

    // UI State: Loading
    submitBtn.disabled = true;
    loadingMessage.textContent = cfg.loading;
    loadingIndicator.classList.remove("hidden");
    resultContainer.classList.add("hidden");
    resultText.innerHTML = "";
    quizDeck.classList.add("hidden");
    quizQuestionsContainer.innerHTML = "";

    try {
      const response = await fetch(cfg.endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: promptText })
      });

      const data = await response.json();

      // UI State: Complete
      loadingIndicator.classList.add("hidden");
      resultContainer.classList.remove("hidden");
      resultModuleBadge.textContent = cfg.badge;

      if (!response.ok) {
        resultTitle.textContent = "Error";
        resultText.innerHTML = `<div class="quiz-explanation-box" style="border-left-color: var(--error);">
          <strong>Request Failed</strong>
          ${data.detail || data.error || "An unexpected server error occurred."}
        </div>`;
        return;
      }

      if (currentTask === "quiz") {
        renderQuizView(data);
      } else {
        renderTextView(data);
      }

      // Scroll to result smoothly
      resultContainer.scrollIntoView({ behavior: "smooth", block: "start" });

    } catch (err) {
      loadingIndicator.classList.add("hidden");
      resultContainer.classList.remove("hidden");
      resultTitle.textContent = "Network Error";
      resultText.innerHTML = `<div class="quiz-explanation-box" style="border-left-color: var(--error);">
        <strong>Connection Error</strong>
        Could not connect to EduGenie server (${err.message}). Is the backend running?
      </div>`;
    } finally {
      submitBtn.disabled = false;
    }
  });

  // Render Standard Text/Markdown Responses
  function renderTextView(data) {
    resultTitle.textContent = `${TASK_CONFIGS[currentTask].badge} Output`;
    quizDeck.classList.add("hidden");
    resultText.classList.remove("hidden");

    const content = data.result || JSON.stringify(data, null, 2);
    resultText.innerHTML = renderMarkdown(content);
  }

  // Render Interactive Quiz View
  function renderQuizView(data) {
    resultTitle.textContent = "Interactive Multiple-Choice Quiz (3 Questions)";
    resultText.classList.add("hidden");
    quizDeck.classList.remove("hidden");

    if (!data.success || !Array.isArray(data.quiz) || data.quiz.length === 0) {
      quizQuestionsContainer.innerHTML = `
        <div class="quiz-explanation-box" style="border-left-color: var(--error);">
          <strong>Quiz Generation Notice</strong>
          ${data.error || "Could not generate a structured quiz for this topic. Please try another passage or check your Gemini API key."}
        </div>
      `;
      return;
    }

    const questions = data.quiz;
    quizState = {
      total: questions.length,
      answered: 0,
      correctCount: 0
    };

    updateScoreboard();
    quizQuestionsContainer.innerHTML = "";

    const prefixes = ["A", "B", "C", "D"];

    questions.forEach((q, qIndex) => {
      const card = document.createElement("div");
      card.className = "quiz-card";
      card.id = `quizCard_${qIndex}`;

      const header = document.createElement("div");
      header.className = "quiz-question-header";
      header.innerHTML = `
        <span class="quiz-q-num">Question ${qIndex + 1} of ${questions.length}</span>
        <h4 class="quiz-q-title">${q.question}</h4>
      `;
      card.appendChild(header);

      const grid = document.createElement("div");
      grid.className = "quiz-options-grid";

      const optionButtons = [];

      q.options.forEach((optText, optIndex) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "option-btn";
        btn.innerHTML = `
          <span class="option-prefix">${prefixes[optIndex] || (optIndex + 1)}</span>
          <span class="option-text">${optText}</span>
        `;

        btn.addEventListener("click", () => {
          handleOptionSelection(btn, optText, q, optionButtons, card);
        });

        optionButtons.push(btn);
        grid.appendChild(btn);
      });

      card.appendChild(grid);
      quizQuestionsContainer.appendChild(card);
    });
  }

  // Handle Option Click in Quiz
  function handleOptionSelection(selectedBtn, selectedText, questionObj, allButtons, cardElement) {
    // Disable all options for this question to prevent re-answering
    allButtons.forEach(btn => btn.disabled = true);

    const correctAnswer = (questionObj.answer || "").trim().toLowerCase();
    const chosenAnswer = (selectedText || "").trim().toLowerCase();

    // Check if chosen option matches or starts with the answer
    const isCorrect = (chosenAnswer === correctAnswer) || 
                      (correctAnswer.length === 1 && selectedBtn.querySelector(".option-prefix").textContent.toLowerCase() === correctAnswer);

    quizState.answered += 1;
    if (isCorrect) {
      quizState.correctCount += 1;
      selectedBtn.classList.add("correct");
    } else {
      selectedBtn.classList.add("incorrect");
      // Highlight the correct answer for student learning
      allButtons.forEach(btn => {
        const txt = btn.querySelector(".option-text").textContent.trim().toLowerCase();
        const pfx = btn.querySelector(".option-prefix").textContent.trim().toLowerCase();
        if (txt === correctAnswer || pfx === correctAnswer) {
          btn.classList.add("correct");
        }
      });
    }

    // Render explanation card
    const explanationBox = document.createElement("div");
    explanationBox.className = "quiz-explanation-box";
    explanationBox.innerHTML = `
      <strong>${isCorrect ? "✅ Correct!" : "❌ Incorrect (Answer: " + questionObj.answer + ")"}</strong>
      ${questionObj.explanation || "No additional explanation provided."}
    `;
    cardElement.appendChild(explanationBox);

    updateScoreboard();
  }

  // Update Scoreboard UI
  function updateScoreboard() {
    const percentage = quizState.answered > 0 ? Math.round((quizState.correctCount / quizState.total) * 100) : 0;
    scoreText.textContent = `${quizState.answered} / ${quizState.total} Answered • Score: ${quizState.correctCount} Correct (${percentage}%)`;
    scoreProgress.style.width = `${(quizState.answered / quizState.total) * 100}%`;
  }

  // Copy Result to Clipboard
  copyBtn.addEventListener("click", () => {
    let textToCopy = "";
    if (currentTask === "quiz") {
      textToCopy = quizQuestionsContainer.innerText;
    } else {
      textToCopy = resultText.innerText;
    }

    if (!textToCopy) return;

    navigator.clipboard.writeText(textToCopy).then(() => {
      const original = copyBtn.innerHTML;
      copyBtn.innerHTML = "✅ Copied!";
      setTimeout(() => {
        copyBtn.innerHTML = original;
      }, 2000);
    }).catch(err => {
      console.error("Clipboard copy failed:", err);
    });
  });

  // Initialize Default State
  setTask("explain");
  updateCharCount();
});
