🤝 CONTRIBUTING

Welcome to FountainData API! We're thrilled you're considering contributing to this next-generation, hyper-fast data ingestion gateway.

FountainData is an Open Core project. We rely on the community to continually improve the core engine—FountainCore—which focuses on validation speed, routing efficiency, and protocol drivers. This commitment ensures the heart of the project remains the fastest and most resilient data quality solution available.

🌟 Our Vision and Core Focus

The mission of FountainData is to eliminate data quality bottlenecks in real-time pipelines. We are laser-focused on:

Validation Speed: Maximizing throughput by leveraging dynamic Pydantic models.

Asynchronous Efficiency: Maintaining a clean, non-blocking asynchronous I/O path throughout the service.

Protocol Flexibility: Building and maintaining drivers for various data sinks (services/data_router.py).

If your contribution helps achieve these goals, you're on the right track!

🔍 What to Contribute (FountainCore Scope)

We encourage contributions in the following areas:

Area

Examples of Contributions We Welcome

Validation Core (validation/core.py)

Adding support for advanced JSON Schema keywords, optimizing Pydantic model generation, and performance benchmarks.

Data Routing (services/data_router.py)

New Drivers! Replacing the mock I/O with asynchronous drivers for open-source systems (e.g., native Kafka client, asynchronous file I/O).

Flow Control (middleware/rate_limiter.py)

Improvements to the Token Bucket algorithm, or implementing alternative rate limiting strategies.

CLI & Testing

Enhancing developer tools, improving test coverage, and fixing bugs.

Documentation

Improving the README, tutorials, and clarifying internal code documentation.

🛑 Out-of-Scope (Premium/Enterprise Boundary)

To maintain our Open Core business model, we cannot accept contributions related to the following areas, as they are reserved for FountainEnterprise offerings:

Authentication/Authorization Logic: Implementation of complex authentication schemes (e.g., OAuth, JWT) beyond the basic API Key mechanism.

Database Persistence: Replacing the CONTRACT_REGISTRY mock with drivers for specific databases (PostgreSQL, MongoDB).

Dedicated Observability/UI: Building dashboards, web UIs, or complex dedicated metrics aggregation endpoints.

💻 Getting Started: Setup & Development

Prerequisites

Python 3.10+

Poetry (Recommended for dependency management) or pip.

1. Fork and Clone

First, fork the repository to your own GitHub account, then clone it locally:

git clone [https://github.com/](https://github.com/)<your-username>/fountaindata.git
cd fountaindata

2. Install Dependencies

pip install -r requirements.txt

3. Run the Development Server

Start the application with hot reloading enabled:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

4. Run Tests

Ensure your changes don't break existing functionality. We use pytest.

pytest

💡 Submission Workflow

We use a standard GitHub flow.

Open an Issue: Before starting any significant work, please search the issues and open a new one to discuss your proposed feature or bug fix. This prevents duplicated effort.

Create a Branch: Create a branch from the main branch with a descriptive name.

git checkout -b feature/your-awesome-feature

Commit: Write clear, concise commit messages following the Conventional Commits specification (e.g., fix(validation): handle non-string event names).

Pull Request (PR): Submit your PR to the main branch of the original repository.

Ensure all tests pass.

Document any new functions or classes.

Describe the problem your PR solves and the solution you implemented.

We will review your code promptly. Thank you for making FountainData the fastest data gateway on the planet!
