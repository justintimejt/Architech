# Gemini Prompt Enhancement Guide

This document explains how to enhance the Gemini prompt to generate more intelligent, context-aware architecture diagrams that differentiate between lightweight and heavy infrastructure, select appropriate technologies, and include descriptive information for all nodes.

## Overview

The current Gemini prompt in `backend/app/routes/chat.py` generates architecture diagrams based on user requests. This guide outlines enhancements to make the AI assistant (Archie) more intelligent about:

1. **Infrastructure Scale Differentiation**: Distinguishing between lightweight (MVP, small-scale) and heavy (enterprise, high-scale) infrastructure
2. **Technology Selection**: Choosing appropriate technologies, frameworks, and services based on infrastructure requirements
3. **Node Descriptions**: Automatically generating detailed descriptions for all nodes explaining their role and purpose

## Current Implementation

The current prompt is located in `backend/app/routes/chat.py` starting at line 522. It includes:
- Basic system instructions for Archie
- Diagram JSON structure
- Available node types
- Positioning rules
- Operation format specifications

## Enhancement Strategy

### 1. Infrastructure Scale Differentiation

#### Problem
The current prompt doesn't distinguish between lightweight and heavy infrastructure requirements. A simple MVP should use different components than an enterprise-scale system.

#### Solution
Add infrastructure scale detection and guidance to the prompt:

```python
# Add to system_instruction in chat.py

INFRASTRUCTURE_SCALE_GUIDANCE = """
INFRASTRUCTURE SCALE DETECTION:
You must analyze the user's request to determine the infrastructure scale:

LIGHTWEIGHT / MVP / SMALL-SCALE indicators:
- "Simple", "basic", "MVP", "prototype", "small", "startup", "personal project"
- Low traffic expectations (< 1000 users)
- Single developer or small team
- Budget constraints mentioned
- Rapid prototyping needs
- Examples: "simple blog", "personal portfolio", "MVP for my app"

HEAVY / ENTERPRISE / HIGH-SCALE indicators:
- "Enterprise", "production", "high traffic", "millions of users", "global"
- High availability requirements
- Scalability concerns mentioned
- Multi-region deployment
- Complex requirements (microservices, distributed systems)
- Examples: "enterprise SaaS", "global e-commerce platform", "high-traffic API"

TECHNOLOGY SELECTION BY SCALE:

LIGHTWEIGHT Infrastructure should use:
- Simple web servers (Express.js, Flask, Sinatra)
- SQLite or PostgreSQL (single instance)
- Basic caching (in-memory or Redis single instance)
- Simple queues (Redis lists, RabbitMQ single node)
- Local file storage or simple S3
- Minimal monitoring (basic logging)
- Single region deployment
- Fewer components overall

HEAVY Infrastructure should use:
- Load-balanced web servers (multiple instances)
- Distributed databases (PostgreSQL clusters, MongoDB sharded, DynamoDB)
- Distributed caching (Redis Cluster, Memcached pools)
- Enterprise queues (Kafka, AWS SQS, RabbitMQ clusters)
- Object storage (S3, Azure Blob, GCS) with CDN
- Comprehensive monitoring (Prometheus, Datadog, New Relic)
- Multi-region deployment with replication
- API Gateways, Service Meshes, Circuit Breakers
- Message brokers for event-driven architecture
- Data warehouses for analytics
- Multiple security layers (WAF, DDoS protection)
"""
```

### 2. Technology and Framework Selection

#### Problem
The current prompt doesn't specify which technologies to use for different node types. Nodes are created with generic names like "Web Server" without technology specifics.

#### Solution
Add technology selection guidance based on infrastructure scale and use case:

```python
TECHNOLOGY_SELECTION_GUIDE = """
TECHNOLOGY SELECTION GUIDELINES:

When creating nodes, you MUST include specific technology names in the "name" field and "attributes" field:

WEB SERVERS (web-server):
- Lightweight: "Express.js Server", "Flask API", "Sinatra App", "Node.js Server"
- Heavy: "Nginx Load Balancer", "Apache HTTP Server", "AWS ALB", "Kubernetes Ingress"

DATABASES (database):
- Lightweight: "SQLite", "PostgreSQL (Single)", "MySQL (Single)", "MongoDB (Single)"
- Heavy: "PostgreSQL Cluster", "MongoDB Sharded", "DynamoDB", "Cassandra", "CockroachDB", "AWS RDS Multi-AZ"

CACHE (cache):
- Lightweight: "Redis (Single)", "In-Memory Cache", "Node Cache"
- Heavy: "Redis Cluster", "Memcached Pool", "AWS ElastiCache", "Hazelcast"

QUEUES (queue):
- Lightweight: "Redis Queue", "RabbitMQ (Single)", "Bull Queue"
- Heavy: "Kafka Cluster", "AWS SQS", "RabbitMQ Cluster", "Google Pub/Sub", "Azure Service Bus"

STORAGE (storage):
- Lightweight: "Local Storage", "Simple S3 Bucket", "File System"
- Heavy: "AWS S3", "Azure Blob Storage", "Google Cloud Storage", "Distributed File System"

MESSAGE BROKERS (message-broker):
- Lightweight: "Redis Pub/Sub", "Simple Event Bus"
- Heavy: "Apache Kafka", "AWS EventBridge", "RabbitMQ Cluster", "NATS", "Google Pub/Sub"

MONITORING (monitoring):
- Lightweight: "Basic Logging", "Console Logs", "Simple Metrics"
- Heavy: "Prometheus + Grafana", "Datadog", "New Relic", "AWS CloudWatch", "Splunk"

CDN (cdn):
- Lightweight: Optional, or "Cloudflare Free"
- Heavy: "AWS CloudFront", "Fastly", "Cloudflare Enterprise", "Akamai"

API GATEWAY (api-gateway):
- Lightweight: "Express Gateway", "Kong (Basic)"
- Heavy: "AWS API Gateway", "Kong Enterprise", "Azure API Management", "Apigee"

WORKERS (worker):
- Lightweight: "Node.js Worker", "Python Worker", "Background Job Processor"
- Heavy: "Kubernetes Job", "AWS Lambda", "Celery Workers", "Sidekiq Workers"

SERVERLESS (serverless-function):
- Lightweight: "Vercel Function", "Netlify Function", "Simple Lambda"
- Heavy: "AWS Lambda (Multi-Region)", "Azure Functions", "Google Cloud Functions"

When specifying technologies, include them in the node's "data.name" field and add a "technology" attribute:
{
  "name": "Express.js API Server",
  "description": "Handles HTTP requests and serves the REST API",
  "attributes": {
    "technology": "Express.js",
    "framework": "Node.js",
    "language": "JavaScript"
  }
}
"""
```

### 3. Node Descriptions

#### Problem
Nodes are created without descriptions explaining their role. Users need to understand what each component does.

#### Solution
Enforce description generation for all nodes:

```python
NODE_DESCRIPTION_REQUIREMENTS = """
NODE DESCRIPTION REQUIREMENTS:

EVERY node you create MUST include a detailed "description" field in the "data" object that explains:
1. What the component does
2. Its role in the architecture
3. Why it's needed
4. How it interacts with other components

Description format:
- Start with the component's primary function
- Explain its role in the specific architecture context
- Mention key interactions with other components
- Include scale-appropriate details

Examples:

LIGHTWEIGHT Example:
{
  "op": "add_node",
  "payload": {
    "id": "web-server-1",
    "type": "web-server",
    "position": {"x": 400, "y": 100},
    "data": {
      "name": "Express.js API Server",
      "description": "Serves as the main API endpoint for the application. Handles HTTP requests from clients, processes business logic, and returns JSON responses. This lightweight Node.js server is suitable for MVP deployments and can handle moderate traffic loads.",
      "attributes": {
        "technology": "Express.js",
        "framework": "Node.js",
        "port": 3000
      }
    }
  }
}

HEAVY Example:
{
  "op": "add_node",
  "payload": {
    "id": "load-balancer-1",
    "type": "load-balancer",
    "position": {"x": 400, "y": 100},
    "data": {
      "name": "AWS Application Load Balancer",
      "description": "Distributes incoming HTTP/HTTPS traffic across multiple web server instances to ensure high availability and fault tolerance. Performs health checks on backend servers, routes traffic based on routing rules, and terminates SSL/TLS connections. Essential for enterprise-scale deployments requiring 99.9% uptime.",
      "attributes": {
        "technology": "AWS ALB",
        "health_check_interval": "30s",
        "ssl_termination": true
      }
    }
  }
}

DATABASE Example:
{
  "op": "add_node",
  "payload": {
    "id": "database-1",
    "type": "database",
    "position": {"x": 400, "y": 300},
    "data": {
      "name": "PostgreSQL Cluster",
      "description": "Primary relational database storing all application data including user accounts, transactions, and business records. Configured as a multi-node cluster with primary-replica replication for high availability. Handles ACID transactions and complex queries required for the application's data integrity needs.",
      "attributes": {
        "technology": "PostgreSQL",
        "deployment": "Multi-AZ Cluster",
        "replication": "Primary-Replica"
      }
    }
  }
}

CRITICAL: Never create a node without a description. The description should be 2-4 sentences explaining the component's purpose and role.
"""
```

## Implementation Steps

### Step 1: Update the System Prompt

Modify the `system_instruction` variable in `backend/app/routes/chat.py` to include all three enhancement sections:

```python
system_instruction = f"""
You are Archie, a friendly and helpful AI assistant that helps users design system architecture diagrams. Your name is Archie, and you should refer to yourself as Archie when responding to users.
The diagram is represented as a JSON "project" with nodes and edges.

Current diagram JSON:
{diagram_json}

Recent chat:
{history_text}

{INFRASTRUCTURE_SCALE_GUIDANCE}

{TECHNOLOGY_SELECTION_GUIDE}

{NODE_DESCRIPTION_REQUIREMENTS}

When the user sends an instruction, you should:
1. Analyze the infrastructure scale (lightweight vs. heavy) based on the user's request
2. Select appropriate technologies based on the scale
3. Provide a friendly, conversational response explaining what you're doing
4. Generate the necessary diagram operations with detailed descriptions for all nodes

You MUST respond with a JSON object in this exact format:
{{
  "message": "A friendly, conversational explanation of what you're doing. Be helpful and clear. Describe what components you're adding, removing, or modifying, and mention the infrastructure scale you've detected (e.g., 'I'm creating a lightweight MVP architecture' or 'I'm setting up an enterprise-scale system').",
  "operations": [
    {{"op": "add_node", "payload": {{"id": "web-server-1", "type": "web-server", "position": {{"x": 400, "y": 100}}, "data": {{"name": "Express.js API Server", "description": "Serves as the main API endpoint...", "attributes": {{"technology": "Express.js"}}}}}}, "metadata": {{"x": 400, "y": 100}}}},
    {{"op": "add_node", "payload": {{"id": "database-1", "type": "database", "position": {{"x": 400, "y": 300}}, "data": {{"name": "PostgreSQL (Single)", "description": "Stores all application data...", "attributes": {{"technology": "PostgreSQL"}}}}}}, "metadata": {{"x": 400, "y": 300}}}},
    {{"op": "add_edge", "payload": {{"source": "web-server-1", "target": "database-1"}}}}
  ]
}}

[... rest of existing prompt ...]
"""
```

### Step 2: Enhance Node Type Information

Update the `AVAILABLE_NODE_TYPES` list to include technology suggestions for each node type. You can add a `technologies` field to each node type definition:

```python
AVAILABLE_NODE_TYPES = [
    {
        "id": "web-server",
        "label": "Web Server",
        "description": "Serves HTTP/HTTPS requests and hosts web applications.",
        "technologies": {
            "lightweight": ["Express.js", "Flask", "Sinatra", "Node.js", "FastAPI"],
            "heavy": ["Nginx", "Apache", "AWS ALB", "Kubernetes Ingress", "HAProxy"]
        },
        "use_cases": [...]
    },
    # ... add technologies to all node types
]
```

Then include this in the prompt:

```python
AVAILABLE_NODE_TYPES_WITH_TECHNOLOGIES = """
Available node types with technology suggestions:

{formatted_node_types_with_technologies}
"""
```

### Step 3: Add Scale Detection Logic

Add explicit instructions for detecting scale from user input:

```python
SCALE_DETECTION_INSTRUCTIONS = """
SCALE DETECTION PROCESS:

1. Read the user's message carefully
2. Look for explicit scale indicators (see INFRASTRUCTURE_SCALE_GUIDANCE above)
3. If scale is ambiguous, ask clarifying questions OR default to lightweight for simplicity
4. Once scale is determined, apply the appropriate technology selection rules
5. Mention the detected scale in your response message

Example responses:
- "I'm creating a lightweight MVP architecture using simple, cost-effective components..."
- "I'm setting up an enterprise-scale system with high availability and distributed components..."
"""
```

## Example Enhanced Prompt Structure

Here's how the complete enhanced prompt should look:

```python
system_instruction = f"""
You are Archie, a friendly and helpful AI assistant that helps users design system architecture diagrams.

{INFRASTRUCTURE_SCALE_GUIDANCE}

{TECHNOLOGY_SELECTION_GUIDE}

{NODE_DESCRIPTION_REQUIREMENTS}

{SCALE_DETECTION_INSTRUCTIONS}

Current diagram JSON:
{diagram_json}

Recent chat:
{history_text}

When the user sends an instruction:
1. Detect infrastructure scale (lightweight vs. heavy)
2. Select appropriate technologies based on scale
3. Generate nodes with detailed descriptions
4. Create appropriate connections
5. Explain your choices in a friendly message

[... rest of existing prompt structure ...]
"""
```

## Testing the Enhancements

### Test Cases

1. **Lightweight MVP Request**:
   - Input: "Create a simple blog with a database"
   - Expected: Simple Express.js server, single PostgreSQL instance, basic descriptions
   - Verify: Technologies are lightweight, descriptions explain MVP context

2. **Heavy Enterprise Request**:
   - Input: "Design a high-traffic e-commerce platform"
   - Expected: Load balancers, distributed databases, CDN, monitoring, detailed descriptions
   - Verify: Technologies are enterprise-grade, descriptions mention scalability

3. **Mixed Scale Request**:
   - Input: "Create a simple API that needs to scale to millions of users"
   - Expected: Start simple but include scalability considerations in descriptions
   - Verify: Descriptions explain both current simplicity and future scalability

4. **Description Verification**:
   - Check that every node has a non-empty description field
   - Verify descriptions explain the component's role
   - Ensure descriptions are contextually appropriate

## Benefits

1. **Better Architecture Decisions**: AI makes more informed choices about technology selection
2. **Improved User Understanding**: Descriptions help users understand each component's purpose
3. **Scale-Appropriate Designs**: Prevents over-engineering for simple projects and under-engineering for complex ones
4. **Educational Value**: Users learn about appropriate technologies for different scales
5. **Professional Output**: Diagrams include detailed, professional descriptions suitable for documentation

## Maintenance

- **Update Technology Lists**: Keep technology suggestions current with industry trends
- **Refine Scale Detection**: Improve detection logic based on user feedback
- **Enhance Descriptions**: Refine description templates to be more informative
- **Add New Node Types**: When adding new node types, include technology suggestions and description templates

## Future Enhancements

1. **Cost Estimation**: Add cost considerations to technology selection
2. **Regional Preferences**: Consider user location for cloud provider suggestions
3. **Technology Stack Consistency**: Ensure selected technologies work well together
4. **Learning from History**: Use chat history to learn user preferences
5. **Interactive Clarification**: Ask users about scale if ambiguous

