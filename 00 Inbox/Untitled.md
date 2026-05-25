<system_specification>
# Production AI Agent Harness Specification

This project has will allow me to automate a GitHub workflow using AI agents. 

## 1. Architectural Foundation & Framework
The harness is built as an API-based orchestrator leveraging the **`pi-mono`** toolkit, moving away from wrapping opaque CLI binaries in favor of programmatic ReAct loop control [1-3]. 

*   **Unified LLM API:** Uses `@mariozechner/pi-ai` to support multi-provider routing (OpenAI, Anthropic, Google), preventing vendor lock-in and allowing dynamic model switching [1].
*   **Agent Runtime:** Utilizes `@mariozechner/pi-agent-core` to manage state, tool registry, and execution cycles [1].
*   **Observability & UI:** Incorporates `@mariozechner/pi-tui` for local terminal monitoring of background threads and worktrees, completely decoupled from the GitHub issue polling service [1].

## 2. The 4-Agent Topology
The system decomposes tasks across one main orchestrator and three specialized, ephemeral subagents to prevent context bloat and enforce schema-level safety [4-6].

### A. Project Manager (Main Agent)
*   **Role:** Continuous background orchestrator. 
*   **Capabilities:** Manages the global Kanban state (`todo.md`), communicates with users via GitHub comments, and spawns subagents [7, 8]. It does *not* possess code-writing tools [9].
*   **Tools:** `write_todos`, `update_todo`, `ask_user`, `spawn_subagent`, `present_plan` [7, 10, 11].

### B. Planner (Subagent / Gatekeeper)
*   **Role:** Codebase exploration, strategy formulation, and error-loop gatekeeper [5, 12].
*   **Capabilities:** Read-only access to explore code and map user intent to actual files [12]. Evaluates Reviewer feedback to break infinite retry loops.
*   **Output:** Drafts a strict 7-section `plan.md` (goal, context, files to modify, new files to create, implementation steps, verification criteria, and risks) [13].

### C. Builder (Subagent)
*   **Role:** Code execution and implementation.
*   **Capabilities:** Full read/write filesystem access and shell execution [14].
*   **Environment:** Runs in an isolated Git worktree (e.g., managed via a `dmux`-like pattern) to prevent conflicts [15, 16].

### D. Reviewer (Subagent)
*   **Role:** Verification and quality assurance (e.g., `PR-Reviewer` or `Security-Reviewer`) [6].
*   **Capabilities:** Read-only code navigation, diff analysis, and test execution [6, 17]. 
*   **Output:** Categorizes feedback as *Critical*, *Moderate*, or *Minor* for the Planner to evaluate.

## 3. Core Execution Workflows

### Use Case: Actionable GitHub Issue
1.  **Intake:** PM polls the GitHub issue, logs it into `todo.md` [7].
2.  **Exploration:** PM calls `spawn_subagent(type="Planner")` [12]. Planner explores the codebase and writes `plan.md` [13].
3.  **Approval:** PM uses `present_plan` to post the strategy to GitHub. User approves [18].
4.  **Execution:** PM creates a Git worktree and spawns a Builder inside it [15, 16]. Builder executes the `plan.md` steps and terminates.
5.  **Verification:** PM spawns a Reviewer in the same worktree [6]. If successful, PM merges the branch and closes the issue [19].

### Use Case: Insufficient Information
1.  Planner hits a blocker during exploration and terminates, returning questions to the PM [5, 20].
2.  PM halts execution and uses `ask_user` to post a structured clarification request on the GitHub issue [10].
3.  The task remains suspended in `todo.md` until the user replies [7].

### Use Case: Error Recovery & Doom-Loop Prevention
1.  **Categorized Review:** Reviewer finds failing tests and outputs structured feedback (Critical/Moderate/Minor).
2.  **Gatekeeper Evaluation:** PM spawns the Planner to evaluate the Reviewer's feedback against the Builder's diff. 
3.  **Resolution or Escalation:** If fixable, Planner updates `plan.md` and PM spawns a new Builder. If the Planner detects a semantic doom loop (e.g., 3 failed attempts at the same bug), it trips a circuit breaker and escalates to the user via GitHub [21].

## 4. Memory & Context Engineering

*   **Filesystem-as-Memory:** Long-horizon state is externalized to files (`todo.md`, `plan.md`) [22].
*   **Tool Output Optimization:** Raw outputs >8,000 characters (e.g., test logs) are offloaded to local scratch files, replacing the context with a short preview marker (e.g., `[Output offloaded...]`) to save tokens [23, 24].
*   **Adaptive Context Compaction:** As context pressure rises, a 5-stage pipeline activates: Warning (70%), Observation Masking (80%), Fast Pruning (85%), Aggressive Masking (90%), and Full LLM Summarization (99%) [25, 26].
*   **Just-In-Time Reminders:** The harness injects `role: user` messages exactly at the point of decision (e.g., reminding the agent of an incomplete todo) to prevent "lost in the middle" instruction fade-out [27-29].

## 5. Resource Limits & Safety

*   **Concurrency Semaphores (Worker Pools):** The PM is restricted to `N` parallel active Git worktrees [15]. Background thread pools cap concurrent subagent execution (e.g., max 5 parallel tools) [30].
*   **Centralized Cost Tracking:** A `CostTracker` service monitors cumulative token usage across all API calls [31, 32]. A global budget kill-switch pauses the PM if financial limits are breached.
*   **Schema-Level Safety:** Write tools (`write_file`, `run_command`) are structurally omitted from Planner and Reviewer schemas, rendering destructive actions impossible for those roles [12, 33].
*   **Stale-Read Prevention:** The harness tracks file modification times. If a Builder attempts to edit a file that has changed since it was last read, the edit is rejected, forcing a re-read [34].
</system_specification>