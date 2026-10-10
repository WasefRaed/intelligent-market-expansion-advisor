# AI Tool Usage Disclosure

This project was developed with AI assistance. The following disclosure explains the tools used, their roles, my direct contributions, and the limitations of the system.

## 1. AI Tools and Technologies Used

**ChatGPT (OpenAI)**
- Assisted with project planning and architecture design.
- Helped draft Python, Agno, and Streamlit implementations.
- Supported debugging, code improvements, and test development.
- Assisted with documentation, evaluation analysis, and reliability improvements.

**Google Gemini API**
- Powers the AI reasoning and recommendation generation.
- Supports the Agno agents in answering executive business questions.
- Generates structured business analysis based on available project data and tools.
- Does not independently verify market facts or perform the application's deterministic financial calculations.

**Agno Framework**
- Provides the main agentic architecture.
- Manages the multi-agent coordinator and five specialist agents.
- Enables task delegation and integration with Python tools.

**Streamlit**
- Provides the interactive chatbot interface and dashboard.
- Enables users to explore locations, financial scenarios, and research evidence.

## 2. My Direct Contribution

My direct contributions included:

- Interpreting the business requirements and planning the project objectives.
- Setting up the Python development environment and configuring the Gemini API.
- Running the application and testing ten executive business scenarios.
- Reviewing generated recommendations and identifying errors or unsupported assumptions.
- Testing and verifying financial calculation corrections.
- Validating real Agno multi-agent delegation and Python tool execution.
- Running automated tests and reviewing terminal logs.
- Publishing and organizing the final project on GitHub.

ChatGPT assisted with code generation, debugging, and documentation. I personally configured, executed, tested, and reviewed the application, and I take responsibility for explaining its architecture, behavior, and limitations.

## 3. Testing and Verification

The project includes:

- 72 passing automated offline tests.
- Ten manually evaluated business scenarios.
- Verified execution of two specialist agents during a multi-agent delegation test.
- Financial calculations performed using deterministic Python logic.
- A reviewed reference registry that distinguishes supported claims from planning assumptions.
- API quota safeguards and fallback handling.

These tests validate specific technical behaviors. They do not guarantee the accuracy of AI-generated market recommendations.

## 4. Limitations and Responsible AI Use

- Location rankings are based on internal qualitative screening assumptions.
- Pricing bands and financial scenarios are illustrative.
- Official reference notes support limited factual claims, not investment outcomes.
- Live research is disabled by default.
- Gemini API availability depends on provider quotas.
- Business recommendations require independent verification before real investment decisions.

The system is designed to support research and executive decision-making, not replace professional financial, legal, or market analysis.

## 5. Accountability

I acknowledge the use of AI assistance throughout development and remain responsible for the final project's testing, documentation, and presentation.

I understand the system's intended architecture and the distinction between AI-generated recommendations, Python-based calculations, internal assumptions, and reviewed external evidence.