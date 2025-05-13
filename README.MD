# LLM-Based Query Handling Architecture

This document provides an overview of a modular architecture designed to handle user queries through a large language model (LLM). The system consists of four main components working together to manage client communication, session context, and LLM interaction.

---

## 🧱 Components

### 1. **MCP Client**
- **Purpose:** Sends query requests to the MCP Server.
- **Responsibilities:**
  - Accepts user input or client API calls.
  - Forwards queries to the MCP Server over a socket connection.
  - Receives and displays responses.

### 2. **MCP Server**
- **Purpose:** Handles incoming requests from clients and routes them through the processing pipeline.
- **Responsibilities:**
  - Listens on a socket for client requests.
  - Communicates with SSMP Server to fetch or update session context.
  - Forwards processed queries and context to the LLM Service.
  - Sends the final response back to the client.

### 3. **SSMP Server**
- **Purpose:** Maintains user session context.
- **Responsibilities:**
  - Stores contextual data such as user preferences, previous queries, and conversation history.
  - Provides relevant context to the MCP Server upon request.
  - Updates session context based on new interactions.

### 4. **LLM Service**
- **Purpose:** Acts as a unified interface to handle all LLM-related operations.
- **Responsibilities:**
  - Accepts user queries along with contextual information.
  - Processes the query using a configured LLM backend (e.g., OpenAI, Claude, etc.).
  - Returns the generated response.

---

## 🔄 Data Flow

```text
[MCP Client]
     ↓
[MCP Server] → [SSMP Server]
     ↓
[LLM Service]
     ↑
[MCP Server] → [MCP Client]
