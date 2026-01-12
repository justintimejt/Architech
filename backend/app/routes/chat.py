from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from ..supabase_client import supabase
from ..env import Env
import google.generativeai as genai
import traceback
import uuid
import json
import re
from postgrest.exceptions import APIError

# Configure Gemini API - handle errors gracefully
try:
    if Env.GEMINI_API_KEY:
        genai.configure(api_key=Env.GEMINI_API_KEY)
    else:
        print("⚠️  Warning: GOOGLE_GEMINI_API_KEY not set in backend/.env")
except Exception as e:
    print(f"⚠️  Warning: Failed to configure Gemini API: {e}")

router = APIRouter()

# All available node types that can be created in the diagram
# Each node type includes its ID, label, description, and common use cases
# This list must stay in sync with frontend/src/nodes/nodeTypes.ts
AVAILABLE_NODE_TYPES = [
    {
        "id": "web-server",
        "label": "Web Server",
        "description": "Serves HTTP/HTTPS requests and hosts web applications. Handles incoming client requests and serves responses.",
        "technologies": {
            "lightweight": ["Express.js", "Flask", "Sinatra", "Node.js", "FastAPI", "Django"],
            "heavy": ["Nginx", "Apache", "AWS ALB", "Kubernetes Ingress", "HAProxy", "Traefik"]
        },
        "use_cases": [
            "Hosting web applications and APIs",
            "Serving static content",
            "Handling HTTP/HTTPS requests",
            "Application servers for business logic"
        ]
    },
    {
        "id": "database",
        "label": "Database",
        "description": "Stores and manages structured data persistently. Provides data persistence and query capabilities.",
        "technologies": {
            "lightweight": ["SQLite", "PostgreSQL (Single)", "MySQL (Single)", "MongoDB (Single)", "SQLite"],
            "heavy": ["PostgreSQL Cluster", "MongoDB Sharded", "DynamoDB", "Cassandra", "CockroachDB", "AWS RDS Multi-AZ", "Azure Cosmos DB"]
        },
        "use_cases": [
            "Storing application data",
            "User data and authentication",
            "Transaction records",
            "Relational or NoSQL data storage"
        ]
    },
    {
        "id": "worker",
        "label": "Worker",
        "description": "Background processing service that handles asynchronous tasks and long-running operations.",
        "technologies": {
            "lightweight": ["Node.js Worker", "Python Worker", "Background Job Processor", "Celery (Single)"],
            "heavy": ["Kubernetes Job", "AWS Lambda", "Celery Workers", "Sidekiq Workers", "Bull Queue Cluster"]
        },
        "use_cases": [
            "Background job processing",
            "Image/video processing",
            "Data transformation tasks",
            "Scheduled tasks and cron jobs"
        ]
    },
    {
        "id": "cache",
        "label": "Cache",
        "description": "High-speed temporary storage for frequently accessed data to improve performance and reduce latency.",
        "technologies": {
            "lightweight": ["Redis (Single)", "In-Memory Cache", "Node Cache", "Memcached (Single)"],
            "heavy": ["Redis Cluster", "Memcached Pool", "AWS ElastiCache", "Hazelcast", "Apache Ignite"]
        },
        "use_cases": [
            "Caching database query results",
            "Session storage",
            "API response caching",
            "Reducing database load"
        ]
    },
    {
        "id": "queue",
        "label": "Queue",
        "description": "Message queue system that enables asynchronous communication and task distribution between services.",
        "technologies": {
            "lightweight": ["Redis Queue", "RabbitMQ (Single)", "Bull Queue", "Beanstalkd"],
            "heavy": ["Kafka Cluster", "AWS SQS", "RabbitMQ Cluster", "Google Pub/Sub", "Azure Service Bus", "NATS"]
        },
        "use_cases": [
            "Task queuing and processing",
            "Decoupling services",
            "Handling peak loads",
            "Reliable message delivery"
        ]
    },
    {
        "id": "storage",
        "label": "Storage",
        "description": "Object storage or file storage system for storing files, media, and unstructured data.",
        "technologies": {
            "lightweight": ["Local Storage", "Simple S3 Bucket", "File System", "MinIO"],
            "heavy": ["AWS S3", "Azure Blob Storage", "Google Cloud Storage", "Distributed File System", "Ceph"]
        },
        "use_cases": [
            "File storage (images, documents)",
            "Object storage (S3-style)",
            "Media files and assets",
            "Backup and archival storage"
        ]
    },
    {
        "id": "third-party-api",
        "label": "Third-party API",
        "description": "External service or API that your system integrates with. Represents dependencies on external services.",
        "technologies": {
            "lightweight": ["Stripe API", "Twilio API", "SendGrid API", "Generic REST API"],
            "heavy": ["Stripe Enterprise", "Twilio Enterprise", "SendGrid Enterprise", "AWS Marketplace APIs"]
        },
        "use_cases": [
            "Payment processing APIs",
            "Authentication services (OAuth)",
            "Email/SMS services",
            "External data providers"
        ]
    },
    {
        "id": "compute-node",
        "label": "Compute Node",
        "description": "Generic compute resource for processing tasks, running containers, or executing code.",
        "technologies": {
            "lightweight": ["Docker Container", "Simple VM", "Local Compute"],
            "heavy": ["Kubernetes Node", "AWS ECS", "Azure Container Instances", "Google Cloud Run"]
        },
        "use_cases": [
            "Container orchestration nodes",
            "Serverless function execution",
            "Batch processing",
            "General-purpose compute resources"
        ]
    },
    {
        "id": "load-balancer",
        "label": "Load Balancer",
        "description": "Distributes incoming network traffic across multiple servers to ensure high availability and performance.",
        "technologies": {
            "lightweight": ["Nginx (Basic)", "HAProxy (Basic)", "Simple Load Balancer"],
            "heavy": ["AWS ALB", "AWS NLB", "Kubernetes Ingress", "HAProxy Enterprise", "F5 BIG-IP"]
        },
        "use_cases": [
            "Distributing traffic across web servers",
            "High availability and redundancy",
            "SSL termination",
            "Traffic routing and health checks"
        ]
    },
    {
        "id": "message-broker",
        "label": "Message Broker",
        "description": "Middleware that enables communication between distributed systems using publish-subscribe or message queue patterns.",
        "technologies": {
            "lightweight": ["Redis Pub/Sub", "Simple Event Bus", "RabbitMQ (Single)"],
            "heavy": ["Apache Kafka", "AWS EventBridge", "RabbitMQ Cluster", "NATS", "Google Pub/Sub", "Azure Event Hubs"]
        },
        "use_cases": [
            "Event-driven architectures",
            "Microservices communication",
            "Real-time messaging",
            "Pub/sub messaging patterns"
        ]
    },
    {
        "id": "cdn",
        "label": "CDN",
        "description": "Content Delivery Network that caches and serves content from edge locations close to users for faster delivery.",
        "technologies": {
            "lightweight": ["Cloudflare Free", "Optional CDN"],
            "heavy": ["AWS CloudFront", "Fastly", "Cloudflare Enterprise", "Akamai", "Azure CDN"]
        },
        "use_cases": [
            "Serving static assets globally",
            "Reducing latency for users",
            "Offloading traffic from origin servers",
            "Video streaming and media delivery"
        ]
    },
    {
        "id": "monitoring",
        "label": "Monitoring Service",
        "description": "Service that collects metrics, logs, and traces to monitor system health, performance, and availability.",
        "technologies": {
            "lightweight": ["Basic Logging", "Console Logs", "Simple Metrics", "Winston", "Pino"],
            "heavy": ["Prometheus + Grafana", "Datadog", "New Relic", "AWS CloudWatch", "Splunk", "Elastic Stack"]
        },
        "use_cases": [
            "Application performance monitoring",
            "Infrastructure metrics",
            "Log aggregation and analysis",
            "Alerting and incident management"
        ]
    },
    {
        "id": "api-gateway",
        "label": "API Gateway",
        "description": "Single entry point for API requests that handles routing, authentication, rate limiting, and request/response transformation.",
        "technologies": {
            "lightweight": ["Express Gateway", "Kong (Basic)", "Simple API Router"],
            "heavy": ["AWS API Gateway", "Kong Enterprise", "Azure API Management", "Apigee", "Tyk"]
        },
        "use_cases": [
            "API request routing and load balancing",
            "Authentication and authorization",
            "Rate limiting and throttling",
            "Request/response transformation"
        ]
    },
    {
        "id": "dns",
        "label": "DNS",
        "description": "Domain Name System service that translates domain names to IP addresses and manages DNS records.",
        "technologies": {
            "lightweight": ["Cloudflare DNS", "Simple DNS", "Route53 Basic"],
            "heavy": ["AWS Route53", "Azure DNS", "Google Cloud DNS", "DNS Made Easy"]
        },
        "use_cases": [
            "Domain name resolution",
            "Load balancing via DNS",
            "CDN routing",
            "Service discovery"
        ]
    },
    {
        "id": "vpc-network",
        "label": "VPC / Network",
        "description": "Virtual Private Cloud or network infrastructure that provides isolated network environments for resources.",
        "technologies": {
            "lightweight": ["Simple Network", "Local Network"],
            "heavy": ["AWS VPC", "Azure Virtual Network", "Google Cloud VPC", "Multi-Region VPC"]
        },
        "use_cases": [
            "Network isolation and security",
            "Private network segments",
            "Subnet management",
            "Network routing and connectivity"
        ]
    },
    {
        "id": "vpn-link",
        "label": "VPN / Private Link",
        "description": "Virtual Private Network or private link that provides secure, encrypted connections between networks or services.",
        "technologies": {
            "lightweight": ["OpenVPN", "WireGuard", "Simple VPN"],
            "heavy": ["AWS VPN", "Azure VPN Gateway", "Google Cloud VPN", "AWS PrivateLink"]
        },
        "use_cases": [
            "Secure remote access",
            "Site-to-site connectivity",
            "Private service connections",
            "Encrypted data transmission"
        ]
    },
    {
        "id": "auth-service",
        "label": "Auth Service",
        "description": "Authentication service that handles user login, session management, and authentication tokens.",
        "technologies": {
            "lightweight": ["JWT Auth", "Passport.js", "Simple Auth Service"],
            "heavy": ["Auth0", "AWS Cognito", "Azure AD", "Okta", "Keycloak"]
        },
        "use_cases": [
            "User authentication",
            "Session management",
            "Token generation and validation",
            "Single sign-on (SSO)"
        ]
    },
    {
        "id": "identity-provider",
        "label": "Identity Provider (IdP)",
        "description": "Identity provider that manages user identities and provides authentication services (e.g., OAuth, SAML).",
        "technologies": {
            "lightweight": ["OAuth 2.0", "Simple IdP", "Social Login"],
            "heavy": ["Okta", "Azure AD", "Google Identity", "AWS SSO", "Ping Identity"]
        },
        "use_cases": [
            "OAuth/OIDC authentication",
            "SAML-based SSO",
            "Social login integration",
            "Centralized identity management"
        ]
    },
    {
        "id": "secrets-manager",
        "label": "Secrets Manager",
        "description": "Service for securely storing and managing secrets, API keys, passwords, and certificates.",
        "technologies": {
            "lightweight": ["Environment Variables", "Simple Secrets", ".env files"],
            "heavy": ["AWS Secrets Manager", "Azure Key Vault", "HashiCorp Vault", "Google Secret Manager"]
        },
        "use_cases": [
            "API key management",
            "Password and credential storage",
            "Certificate management",
            "Secure configuration storage"
        ]
    },
    {
        "id": "waf",
        "label": "Web Application Firewall",
        "description": "Security service that filters and monitors HTTP/HTTPS traffic to protect web applications from attacks.",
        "technologies": {
            "lightweight": ["Cloudflare WAF (Free)", "Basic Firewall"],
            "heavy": ["AWS WAF", "Azure Application Gateway WAF", "Cloudflare Enterprise WAF", "F5 Advanced WAF"]
        },
        "use_cases": [
            "SQL injection prevention",
            "XSS attack protection",
            "DDoS mitigation",
            "Rate limiting and bot protection"
        ]
    },
    {
        "id": "search-engine",
        "label": "Search Engine",
        "description": "Search service that provides full-text search capabilities for applications and data.",
        "technologies": {
            "lightweight": ["Elasticsearch (Single)", "Simple Search", "PostgreSQL Full-Text"],
            "heavy": ["Elasticsearch Cluster", "AWS OpenSearch", "Azure Cognitive Search", "Solr Cloud"]
        },
        "use_cases": [
            "Full-text search",
            "Product search",
            "Document search",
            "Real-time search indexing"
        ]
    },
    {
        "id": "data-warehouse",
        "label": "Data Warehouse",
        "description": "Centralized repository for storing and analyzing large volumes of structured data for business intelligence.",
        "technologies": {
            "lightweight": ["PostgreSQL (Analytics)", "Simple Data Warehouse"],
            "heavy": ["Snowflake", "AWS Redshift", "Google BigQuery", "Azure Synapse", "Databricks"]
        },
        "use_cases": [
            "Business intelligence and analytics",
            "Data aggregation and reporting",
            "Historical data analysis",
            "ETL data processing"
        ]
    },
    {
        "id": "stream-processor",
        "label": "Stream Processor",
        "description": "Service that processes continuous streams of data in real-time for analytics and event processing.",
        "technologies": {
            "lightweight": ["Kafka Streams (Basic)", "Simple Stream Processor"],
            "heavy": ["Apache Flink", "Apache Spark Streaming", "AWS Kinesis", "Google Cloud Dataflow"]
        },
        "use_cases": [
            "Real-time data processing",
            "Event stream processing",
            "Real-time analytics",
            "Streaming ETL pipelines"
        ]
    },
    {
        "id": "etl-job",
        "label": "ETL / Batch Job",
        "description": "Extract, Transform, Load job that processes data in batches for data integration and transformation.",
        "technologies": {
            "lightweight": ["Python Script", "Simple ETL", "Cron Job"],
            "heavy": ["Apache Airflow", "AWS Glue", "Azure Data Factory", "dbt", "Talend"]
        },
        "use_cases": [
            "Data integration",
            "Batch data processing",
            "Data transformation pipelines",
            "Scheduled data migrations"
        ]
    },
    {
        "id": "scheduler",
        "label": "Scheduler / Cron",
        "description": "Service that schedules and executes tasks, jobs, or workflows at specified times or intervals.",
        "technologies": {
            "lightweight": ["Cron", "Node-cron", "Simple Scheduler"],
            "heavy": ["AWS EventBridge", "Azure Scheduler", "Google Cloud Scheduler", "Quartz Scheduler"]
        },
        "use_cases": [
            "Scheduled task execution",
            "Cron job management",
            "Workflow scheduling",
            "Periodic data processing"
        ]
    },
    {
        "id": "serverless-function",
        "label": "Serverless Function",
        "description": "Event-driven compute service that runs code in response to events without managing servers.",
        "technologies": {
            "lightweight": ["Vercel Function", "Netlify Function", "Simple Lambda", "Cloudflare Workers"],
            "heavy": ["AWS Lambda (Multi-Region)", "Azure Functions", "Google Cloud Functions", "AWS Step Functions"]
        },
        "use_cases": [
            "Event-driven processing",
            "API endpoints",
            "Background task processing",
            "Microservices architecture"
        ]
    },
    {
        "id": "logging-service",
        "label": "Logging Service",
        "description": "Service that collects, stores, and analyzes application and system logs for debugging and monitoring.",
        "technologies": {
            "lightweight": ["Winston", "Pino", "Console Logs", "File Logging"],
            "heavy": ["ELK Stack", "AWS CloudWatch Logs", "Azure Monitor", "Splunk", "Datadog Logs"]
        },
        "use_cases": [
            "Centralized log collection",
            "Log aggregation and storage",
            "Log analysis and search",
            "Debugging and troubleshooting"
        ]
    },
    {
        "id": "alerting-service",
        "label": "Alerting / Incident Management",
        "description": "Service that monitors system health and sends alerts or manages incidents when issues are detected.",
        "technologies": {
            "lightweight": ["Email Alerts", "Simple Notifications"],
            "heavy": ["PagerDuty", "Opsgenie", "VictorOps", "AWS SNS", "Datadog Alerts"]
        },
        "use_cases": [
            "System health monitoring",
            "Alert notification",
            "Incident management",
            "On-call management"
        ]
    },
    {
        "id": "status-page",
        "label": "Status Page / Health Check",
        "description": "Public status page or health check service that displays system availability and service status.",
        "technologies": {
            "lightweight": ["Simple Status Page", "Health Check Endpoint"],
            "heavy": ["Statuspage.io", "Atlassian Statuspage", "Cachet", "Uptime Robot"]
        },
        "use_cases": [
            "Public service status",
            "Health check endpoints",
            "Service availability monitoring",
            "Incident communication"
        ]
    },
    {
        "id": "orchestrator",
        "label": "Workflow Orchestrator",
        "description": "Service that orchestrates and manages complex workflows, pipelines, and multi-step processes.",
        "technologies": {
            "lightweight": ["Simple Workflow", "Basic Orchestrator"],
            "heavy": ["Apache Airflow", "AWS Step Functions", "Temporal", "Conductor", "Prefect"]
        },
        "use_cases": [
            "Workflow management",
            "Pipeline orchestration",
            "Multi-step process coordination",
            "Distributed task coordination"
        ]
    },
    {
        "id": "notification-service",
        "label": "Notification Service",
        "description": "Service that sends notifications to users via various channels (push, in-app, etc.).",
        "technologies": {
            "lightweight": ["Simple Notifications", "Firebase Cloud Messaging (Basic)"],
            "heavy": ["AWS SNS", "OneSignal", "Pusher", "Twilio Notify", "SendGrid Notifications"]
        },
        "use_cases": [
            "Push notifications",
            "In-app notifications",
            "User alerts",
            "Multi-channel notifications"
        ]
    },
    {
        "id": "email-service",
        "label": "Email Service",
        "description": "Service that handles email sending, receiving, and management for applications.",
        "technologies": {
            "lightweight": ["SendGrid", "Mailgun", "Simple SMTP"],
            "heavy": ["AWS SES", "SendGrid Enterprise", "Mailgun Enterprise", "Postmark", "SparkPost"]
        },
        "use_cases": [
            "Transactional emails",
            "Email marketing",
            "Email delivery",
            "Email templates and management"
        ]
    },
    {
        "id": "webhook-endpoint",
        "label": "Webhook Endpoint",
        "description": "HTTP endpoint that receives webhook callbacks from external services for event-driven integrations.",
        "technologies": {
            "lightweight": ["Express.js Webhook", "Simple HTTP Endpoint"],
            "heavy": ["AWS API Gateway Webhooks", "Zapier", "Microsoft Power Automate", "Webhook.site"]
        },
        "use_cases": [
            "Third-party service callbacks",
            "Event-driven integrations",
            "Real-time data synchronization",
            "External service notifications"
        ]
    },
    {
        "id": "web-client",
        "label": "Web Client",
        "description": "Web browser or web application client that interacts with backend services.",
        "technologies": {
            "lightweight": ["React", "Vue.js", "Angular", "Vanilla JS"],
            "heavy": ["React (SSR)", "Next.js", "Nuxt.js", "Angular Universal", "Progressive Web App"]
        },
        "use_cases": [
            "Web application frontend",
            "Browser-based clients",
            "User interface",
            "Client-side applications"
        ]
    },
    {
        "id": "mobile-app",
        "label": "Mobile App",
        "description": "Mobile application (iOS, Android) that interacts with backend services via APIs.",
        "technologies": {
            "lightweight": ["React Native", "Flutter", "Ionic"],
            "heavy": ["Native iOS (Swift)", "Native Android (Kotlin)", "Flutter Enterprise", "React Native Enterprise"]
        },
        "use_cases": [
            "Mobile application frontend",
            "Native mobile apps",
            "Mobile user interface",
            "Cross-platform mobile apps"
        ]
    },
    {
        "id": "admin-panel",
        "label": "Admin Panel",
        "description": "Administrative interface for managing and configuring system components and settings.",
        "technologies": {
            "lightweight": ["React Admin", "Simple Dashboard", "Custom Admin UI"],
            "heavy": ["Retool", "AdminJS", "Forest Admin", "Grafana", "Custom Enterprise Dashboard"]
        },
        "use_cases": [
            "System administration",
            "Configuration management",
            "User management",
            "Dashboard and monitoring"
        ]
    }
]

class ChatRequest(BaseModel):
    projectId: str
    message: str

@router.post("/chat")
async def chat(req: ChatRequest):
    try:
        # Validate projectId is a valid UUID
        try:
            uuid.UUID(req.projectId)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid projectId format. Expected UUID, got: {req.projectId}"
            )
        
        # Check if Supabase is configured
        if supabase is None:
            raise HTTPException(
                status_code=503,
                detail="Supabase is not configured. Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in backend/.env"
            )
        
        # Check if Gemini API key is configured
        if not Env.GEMINI_API_KEY:
            raise HTTPException(
                status_code=503,
                detail="Gemini API key is not configured. Please set GOOGLE_GEMINI_API_KEY in backend/.env"
            )
        
        # 1) Load diagram context
        try:
            project_res = supabase.table("projects").select("diagram_json").eq("id", req.projectId).single().execute()
        except APIError as e:
            # Handle Supabase API errors specifically
            # APIError contains a dict with 'message', 'code', etc.
            error_dict = e.args[0] if e.args and isinstance(e.args[0], dict) else {}
            error_msg = error_dict.get('message', str(e))
            error_code = error_dict.get('code', '')
            
            print(f"Supabase APIError: {error_msg} (code: {error_code})")
            
            # Check if it's a UUID format error (PostgreSQL error code 22P02)
            if "invalid input syntax for type uuid" in error_msg.lower() or error_code == '22P02':
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid projectId format: {req.projectId}. Must be a valid UUID."
                )
            # Check if it's a "not found" error (PostgREST error code PGRST116)
            elif "not found" in error_msg.lower() or "no rows" in error_msg.lower() or "PGRST116" in error_code:
                raise HTTPException(
                    status_code=404,
                    detail=f"Project not found: {req.projectId}"
                )
            else:
                raise HTTPException(status_code=500, detail=f"Database error: {error_msg}")
        except Exception as e:
            # Handle any other exceptions
            error_msg = str(e)
            print(f"Error loading project: {e}")
            print(traceback.format_exc())
            if "invalid input syntax for type uuid" in error_msg.lower():
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid projectId format: {req.projectId}. Must be a valid UUID."
                )
            raise HTTPException(status_code=500, detail=f"Error loading project: {error_msg}")

        # Supabase Python client raises exceptions on error, so if we get here, check data
        if not project_res.data:
            raise HTTPException(status_code=404, detail="Project not found in database")

        project = project_res.data
        diagram_json = project.get("diagram_json", {})

        # 2) Load recent chat context
        try:
            messages_res = (
                supabase.table("chat_messages")
                .select("role, content, created_at")
                .eq("project_id", req.projectId)
                .order("created_at", desc=False)
                .limit(20)
                .execute()
            )
            history_rows = messages_res.data or []
        except Exception as e:
            print(f"Error loading chat history: {e}")
            history_rows = []

        history_text = (
            "\n".join(f"{row['role'].upper()}: {row['content']}" for row in history_rows)
            if history_rows
            else "No previous messages."
        )

        # 3) Build system prompt for Gemini
        system_instruction = f"""
You are Archie, a friendly and helpful AI assistant that helps users design system architecture diagrams. Your name is Archie, and you should refer to yourself as Archie when responding to users.
The diagram is represented as a JSON "project" with nodes and edges.

Current diagram JSON:
{diagram_json}

Recent chat:
{history_text}

=== CRITICAL: EDITING EXISTING DIAGRAMS ===
IMPORTANT: Before creating new nodes, ALWAYS check the "Current diagram JSON" above to see what already exists.

When the user asks to EDIT, MODIFY, UPDATE, CHANGE, or REMOVE components:
1. Look at the Current diagram JSON to find existing nodes by their "id" field
2. Use "update_node" operation to modify existing nodes (change name, description, attributes)
3. Use "delete_node" operation to remove existing nodes
4. Use "delete_edge" operation to remove existing connections
5. Only use "add_node" for components that don't already exist in the diagram
6. When updating a node, use the EXACT same "id" from the existing diagram
7. Preserve existing node IDs when possible - don't create duplicates

When the user asks to ADD new components:
- Use "add_node" for new components
- Use "add_edge" for new connections

Examples:
- "Add a cache" → Use add_node (new component)
- "Update the database" → Use update_node with existing database ID
- "Remove the load balancer" → Use delete_node with existing load balancer ID
- "Change the web server to use Express.js" → Use update_node with existing web server ID
- "Edit the database description" → Use update_node with existing database ID

=== INFRASTRUCTURE SCALE DETECTION ===
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

=== TECHNOLOGY SELECTION GUIDELINES ===
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
{{
  "name": "Express.js API Server",
  "description": "Handles HTTP requests and serves the REST API",
  "attributes": {{
    "technology": "Express.js",
    "framework": "Node.js",
    "language": "JavaScript"
  }}
}}

=== NODE DESCRIPTION REQUIREMENTS ===
EVERY node you create MUST include a concise "description" field in the "data" object that explains:
1. What the component does
2. Its role in the architecture

Description format:
- Start with the component's primary function
- Keep it brief (1-2 sentences maximum)
- Include scale-appropriate details if relevant

CRITICAL: Never create a node without a description. The description should be 1-2 sentences explaining the component's purpose and role.

=== SCALE DETECTION PROCESS ===
1. Read the user's message carefully
2. Look for explicit scale indicators (see INFRASTRUCTURE SCALE DETECTION above)
3. If scale is ambiguous, ask clarifying questions OR default to lightweight for simplicity
4. Once scale is determined, apply the appropriate technology selection rules
5. Mention the detected scale in your response message

Example responses:
- "I'm creating a lightweight MVP architecture using simple, cost-effective components..."
- "I'm setting up an enterprise-scale system with high availability and distributed components..."

=== WHEN THE USER SENDS AN INSTRUCTION ===
You should:
1. FIRST: Check the Current diagram JSON to see what nodes and edges already exist
2. Determine if the request is to EDIT existing components or ADD new ones
3. If editing: Use update_node/delete_node operations with existing node IDs from the diagram
4. If adding: Use add_node operations for new components
5. Analyze the infrastructure scale (lightweight vs. heavy) based on the user's request
6. Select appropriate technologies based on the scale
7. Provide a friendly, conversational response explaining what you're doing
8. Generate the necessary diagram operations with detailed descriptions for all nodes

You MUST respond with a JSON object in this exact format:
{{
  "message": "A friendly, conversational explanation of what you're doing. Be helpful and clear. Describe what components you're adding, removing, or modifying, and mention the infrastructure scale you've detected (e.g., 'I'm creating a lightweight MVP architecture' or 'I'm setting up an enterprise-scale system').",
  "operations": [
    {{"op": "add_node", "payload": {{"id": "web-server-1", "type": "web-server", "position": {{"x": 400, "y": 100}}, "data": {{"name": "Express.js API Server", "description": "Main API endpoint handling HTTP requests and serving JSON responses. Suitable for MVP deployments.", "attributes": {{"technology": "Express.js", "framework": "Node.js"}}}}}}, "metadata": {{"x": 400, "y": 100}}}},
    {{"op": "add_node", "payload": {{"id": "database-1", "type": "database", "position": {{"x": 400, "y": 300}}, "data": {{"name": "PostgreSQL (Single)", "description": "Stores application data with ACID transactions. Single-instance database for MVP deployments.", "attributes": {{"technology": "PostgreSQL"}}}}}}, "metadata": {{"x": 400, "y": 300}}}},
    {{"op": "add_edge", "payload": {{"source": "web-server-1", "target": "database-1"}}}}
  ]
}}

IMPORTANT: When positioning nodes, use appropriate spacing:
- Horizontal spacing: 250 pixels between nodes (e.g., x: 100, 350, 600, 850)
- Vertical spacing: 250 pixels between rows (e.g., y: 100, 350, 600, 850)
- Arrange nodes in a grid layout with 4 nodes per row
- Start positions: x starts at 100, y starts at 100
- Example positions for multiple nodes:
  - Row 1: (100, 100), (350, 100), (600, 100), (850, 100)
  - Row 2: (100, 350), (350, 350), (600, 350), (850, 350)
  - Row 3: (100, 600), (350, 600), (600, 600), (850, 600)

Available operations:
- "add_node": {{"op": "add_node", "payload": {{"id": string (REQUIRED - use a descriptive ID like "web-server-1", "database-1", etc.), "type": string, "position": {{"x": number, "y": number}}, "data": {{"name": string (MUST include technology name), "description": string (REQUIRED - 1-2 sentences), "attributes": object (MUST include technology information)}}}}, "metadata": {{"x": number, "y": number}}}} - USE ONLY for NEW components that don't exist in Current diagram JSON
- "update_node": {{"op": "update_node", "payload": {{"id": string (MUST match existing node ID from Current diagram JSON), "data": {{"name": string, "description": string, "attributes": object}}}}}} - USE for modifying existing nodes (edit name, description, attributes)
- "delete_node": {{"op": "delete_node", "payload": {{"id": string (MUST match existing node ID from Current diagram JSON)}}}} - USE for removing existing nodes
- "add_edge": {{"op": "add_edge", "payload": {{"source": string (MUST match a node ID from Current diagram JSON or a new add_node operation), "target": string (MUST match a node ID from Current diagram JSON or a new add_node operation), "type": string (optional)}}}} - USE for new connections
- "delete_edge": {{"op": "delete_edge", "payload": {{"id": string (MUST match existing edge ID from Current diagram JSON)}}}} - USE for removing existing connections

Available node types: web-server, database, worker, cache, queue, storage, third-party-api, compute-node, load-balancer, message-broker, cdn, monitoring, api-gateway, dns, vpc-network, vpn-link, auth-service, identity-provider, secrets-manager, waf, search-engine, data-warehouse, stream-processor, etl-job, scheduler, serverless-function, logging-service, alerting-service, status-page, orchestrator, notification-service, email-service, webhook-endpoint, web-client, mobile-app, admin-panel

CRITICAL RULES FOR POSITIONING NODES:
1. Position nodes in a HIERARCHICAL layout: vertical flow overall, but horizontal arrangement for nodes at the same level
2. Nodes at the SAME LEVEL (e.g., multiple web servers, multiple databases) should be arranged HORIZONTALLY with x values like 200, 400, 600, etc. (200px spacing)
3. Different LEVELS should be arranged VERTICALLY with y values: level 0 at y: 100, level 1 at y: 300, level 2 at y: 500, etc. (200px vertical spacing between levels)
4. Determine levels based on architecture: entry points (load-balancer, CDN) = level 0, application layer (web-server, worker) = level 1, data layer (database, cache) = level 2, etc.
5. If creating multiple nodes at the same level, space them horizontally: first at x: 200, second at x: 400, third at x: 600, etc., all with the same y value
6. Example: 2 web servers at level 1 should be at (x: 200, y: 300) and (x: 400, y: 300), then a database at level 2 at (x: 400, y: 500)

CRITICAL RULES FOR CREATING CONNECTIONS:
1. When creating nodes with "add_node", you MUST include an explicit "id" field in the payload (e.g., "web-server-1", "database-1", "cache-1")
2. When creating edges with "add_edge", the "source" and "target" fields MUST reference the exact "id" values from the corresponding "add_node" operations
3. Always create nodes BEFORE creating edges that connect them (nodes must exist before they can be connected)
4. If you're creating multiple connected components, create all nodes first, then create all edges that connect them

IMPORTANT:
- The "message" field should be conversational and helpful, describing what you did (e.g., "I've added a database node to your diagram!")
- The "operations" array should contain the actual diagram modifications
- If the user asks a question or needs help (not a diagram modification), respond with a helpful message and an empty operations array: {{"message": "...", "operations": []}}
- Return ONLY valid JSON. Do NOT wrap it in markdown code blocks (```json or ```).
- Do NOT include any text outside the JSON object.
- EVERY node MUST have a "description" field with 1-2 sentences explaining its role.
- EVERY node MUST include technology information in the "name" and "attributes" fields.
"""

        # 4) Call Gemini API
        try:
            # First, list all available models to see what's actually available
            available_models = []
            try:
                print("📋 Listing all available Gemini models...")
                for model in genai.list_models():
                    model_display_name = model.name.split('/')[-1] if '/' in model.name else model.name
                    if 'generateContent' in model.supported_generation_methods:
                        available_models.append({
                            'name': model_display_name,
                            'full_name': model.name,
                            'methods': model.supported_generation_methods
                        })
                        print(f"  ✅ {model_display_name} (full: {model.name})")
                
                if not available_models:
                    print("⚠️  No models with generateContent support found")
                else:
                    print(f"📊 Found {len(available_models)} available model(s)")
            except Exception as e:
                print(f"⚠️  Warning: Could not list models: {e}")
                print(traceback.format_exc())
            
            # Prioritize free-tier compatible models
            # Updated list based on actual available models (gemini-1.5-flash is no longer available)
            # Free tier typically supports: gemini-2.5-flash, gemini-2.0-flash, gemini-flash-latest
            preferred_models = [
                "gemini-2.5-flash",           # Latest stable free-tier model
                "gemini-2.0-flash",           # Alternative free-tier option
                "gemini-flash-latest",         # Latest flash model
                "gemini-2.5-flash-lite",      # Lite version
                "gemini-2.0-flash-lite",      # Alternative lite
                "gemini-pro-latest",          # Pro model (may have limits)
                "gemini-1.5-flash",           # Legacy (may not be available)
                "gemini-1.5-pro",             # Legacy (may not be available)
            ]
            
            model_name = None
            model_full_name = None
            
            # First, try to find preferred models from the list
            if available_models:
                for preferred in preferred_models:
                    for model_info in available_models:
                        # Exact match or starts with preferred name
                        if (model_info['name'] == preferred or 
                            model_info['name'].startswith(preferred) or
                            preferred in model_info['name']):
                            # Check if it's a free-tier model (not experimental, not preview)
                            if ('-exp' not in model_info['name'].lower() and 
                                '-preview' not in model_info['name'].lower()):
                                model_name = model_info['name']
                                model_full_name = model_info['full_name']
                                print(f"✅ Selected free-tier model: {model_name} (full: {model_full_name})")
                                break
                    if model_name:
                        break
            
            # If no preferred model found, use the first available non-experimental, non-preview model
            if not model_name and available_models:
                for model_info in available_models:
                    if ('-exp' not in model_info['name'].lower() and 
                        '-preview' not in model_info['name'].lower()):
                        model_name = model_info['name']
                        model_full_name = model_info['full_name']
                        print(f"✅ Selected available model: {model_name} (full: {model_full_name})")
                        break
            
            # Fallback: try creating models directly (for backwards compatibility)
            if not model_name:
                print("⚠️  No model found from list, trying direct model creation...")
                for name in preferred_models:
                    try:
                        test_model = genai.GenerativeModel(name)
                        model_name = name
                        model_full_name = name
                        print(f"✅ Using model (direct): {model_name}")
                        break
                    except Exception as e:
                        print(f"  Model {name} not available: {e}")
                        continue
            
            if not model_name:
                error_detail = "No available Gemini models found. "
                if available_models:
                    error_detail += f"Available models: {', '.join([m['name'] for m in available_models[:5]])}"
                else:
                    error_detail += "Please check your API key and model availability."
                raise HTTPException(status_code=503, detail=error_detail)
            
            # Use display name (GenerativeModel accepts just the model name, not the full path)
            # The full name is like "models/gemini-2.5-flash" but we need just "gemini-2.5-flash"
            model_to_use = model_name  # Use display name, not full path
            print(f"🔧 Creating GenerativeModel with: {model_to_use}")
            model = genai.GenerativeModel(model_to_use)
            prompt = system_instruction + "\nUSER:\n" + req.message
            response = model.generate_content(prompt)
            reply_text = (response.text or "").strip()
            
            # Clean up response: remove markdown code blocks if present
            # Handle various formats: ```json, ```, text before/after code blocks
            # Try to find JSON in markdown code blocks (```json ... ``` or ``` ... ```)
            code_block_pattern = r'```(?:json)?\s*\n?(.*?)```'
            code_block_match = re.search(code_block_pattern, reply_text, re.DOTALL)
            if code_block_match:
                reply_text = code_block_match.group(1).strip()
            elif reply_text.startswith('```'):
                # Fallback: simple code block removal
                first_newline = reply_text.find('\n')
                if first_newline != -1:
                    reply_text = reply_text[first_newline + 1:]
                else:
                    reply_text = reply_text[3:]  # Remove ``` if no newline
                # Remove trailing ```
                last_backticks = reply_text.rfind('```')
                if last_backticks != -1:
                    reply_text = reply_text[:last_backticks]
                reply_text = reply_text.strip()
            
            # Try to extract JSON object if there's text before/after
            # Look for first { and last } to extract JSON object
            first_brace = reply_text.find('{')
            last_brace = reply_text.rfind('}')
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                # Extract just the JSON object
                potential_json = reply_text[first_brace:last_brace + 1]
                # Only use it if it looks like valid JSON structure
                if potential_json.count('{') == potential_json.count('}'):
                    reply_text = potential_json
        except Exception as e:
            error_msg = str(e)
            print(f"Error calling Gemini API: {e}")
            print(traceback.format_exc())
            
            # Handle rate limit errors with helpful messages
            if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                if "free_tier" in error_msg.lower():
                    raise HTTPException(
                        status_code=429,
                        detail="Gemini API free tier quota exceeded. Please wait a few minutes or upgrade your API plan. Free tier typically supports gemini-2.5-flash, gemini-2.0-flash, and gemini-flash-latest models."
                    )
                else:
                    raise HTTPException(
                        status_code=429,
                        detail="Gemini API rate limit exceeded. Please wait a few minutes before trying again."
                    )
            
            raise HTTPException(status_code=500, detail=f"Gemini API error: {error_msg}")

        if not reply_text:
            raise HTTPException(status_code=500, detail="Empty response from Gemini")

        # Parse the response JSON
        try:
            response_data = json.loads(reply_text)
            
            # Extract message and operations
            assistant_message = response_data.get("message", "I've processed your request.")
            operations = response_data.get("operations", [])
            
            # Validate operations is a list
            if not isinstance(operations, list):
                operations = []
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Failed to parse AI response as JSON: {e}")
            print(f"📝 Raw response (first 500 chars): {reply_text[:500]}")
            print(f"📝 Raw response length: {len(reply_text)} chars")
            
            # Initialize fallback values
            operations = []
            assistant_message = None
            
            # Try to extract JSON from the response more aggressively
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            json_matches = re.findall(json_pattern, reply_text, re.DOTALL)
            
            if json_matches:
                # Try the largest match first (likely the main JSON object)
                json_matches.sort(key=len, reverse=True)
                for json_candidate in json_matches:
                    try:
                        response_data = json.loads(json_candidate)
                        if "message" in response_data or "operations" in response_data:
                            assistant_message = response_data.get("message", "I've processed your request.")
                            operations = response_data.get("operations", [])
                            if not isinstance(operations, list):
                                operations = []
                            print(f"✅ Successfully extracted JSON from response")
                            break
                    except json.JSONDecodeError:
                        continue
            
            # If we still don't have a message, try fallback parsing
            if assistant_message is None:
                # Fallback: treat as old format (just operations array)
                try:
                    parsed = json.loads(reply_text)
                    if isinstance(parsed, list):
                        operations = parsed
                        assistant_message = "I've updated your diagram."
                    else:
                        operations = []
                        assistant_message = "I received your message, but couldn't parse the response format."
                except json.JSONDecodeError:
                    operations = []
                    error_preview = str(e)[:100] if len(str(e)) > 100 else str(e)
                    assistant_message = f"I received your message, but encountered an error processing it. The AI response couldn't be parsed as JSON. Please try rephrasing your request. (Error: {error_preview})"
                    print(f"❌ All JSON parsing attempts failed. Full error: {e}")
                    print(f"📄 Full response: {reply_text}")

        # 5) Store messages (user + assistant) for history
        try:
            # Validate that the project exists in Supabase before saving messages
            # This ensures we're using the correct project_id
            try:
            project_check = supabase.table("projects").select("id").eq("id", req.projectId).single().execute()
            except APIError as api_err:
                error_dict = api_err.args[0] if api_err.args and isinstance(api_err.args[0], dict) else {}
                error_msg = error_dict.get('message', str(api_err))
                print(f"❌ Error checking project existence: {error_msg}")
                project_check = None
            
            if not project_check or not project_check.data or not project_check.data.get("id"):
                print(f"⚠️  Warning: Project {req.projectId} not found in Supabase. Skipping chat message save.")
                # Don't fail the request, but log the issue
            else:
                # Ensure project_id is exactly what we validated
                validated_project_id = project_check.data["id"]
                
                if validated_project_id != req.projectId:
                    print(f"⚠️  Warning: Project ID mismatch. Requested: {req.projectId}, Found: {validated_project_id}")
                    print(f"⚠️  Using validated project ID: {validated_project_id}")
                
                try:
                result = supabase.table("chat_messages").insert([
                    {
                        "project_id": validated_project_id,
                        "role": "user",
                        "content": req.message,
                    },
                    {
                        "project_id": validated_project_id,
                        "role": "assistant",
                        "content": assistant_message,
                    },
                ]).execute()
                
                    # Check for errors explicitly (CRITICAL FIX)
                    if hasattr(result, 'error') and result.error:
                        error_obj = result.error
                        error_code = getattr(error_obj, 'code', 'N/A')
                        error_message = getattr(error_obj, 'message', str(error_obj))
                        error_details = getattr(error_obj, 'details', 'N/A')
                        print(f"❌ ERROR saving chat messages for project {validated_project_id}:")
                        print(f"   Error code: {error_code}")
                        print(f"   Error message: {error_message}")
                        print(f"   Error details: {error_details}")
                        print(f"   This may be due to RLS policies blocking the insert.")
                        print(f"   Verify service role key is configured correctly in backend/.env")
                    elif result.data:
                        print(f"✅ Successfully saved {len(result.data)} chat messages for project {validated_project_id}")
                    # Verify both messages were saved with the same project_id
                    if len(result.data) == 2:
                        user_msg_project_id = result.data[0].get("project_id")
                        assistant_msg_project_id = result.data[1].get("project_id")
                        if user_msg_project_id != assistant_msg_project_id:
                            print(f"❌ ERROR: Project ID mismatch in saved messages!")
                            print(f"   User message project_id: {user_msg_project_id}")
                            print(f"   Assistant message project_id: {assistant_msg_project_id}")
                        elif user_msg_project_id != validated_project_id:
                            print(f"❌ ERROR: Saved messages have wrong project_id!")
                            print(f"   Expected: {validated_project_id}")
                            print(f"   Got: {user_msg_project_id}")
                else:
                    print(f"⚠️  Chat messages insert returned no data for project {validated_project_id}")
                        print(f"   No error was reported, but no data was returned.")
                        print(f"   This may indicate a silent failure. Check Supabase logs.")
                        
                except APIError as api_err:
                    # Handle Supabase API errors specifically
                    error_dict = api_err.args[0] if api_err.args and isinstance(api_err.args[0], dict) else {}
                    error_msg = error_dict.get('message', str(api_err))
                    error_code = error_dict.get('code', 'N/A')
                    error_hint = error_dict.get('hint', 'N/A')
                    print(f"❌ Supabase API error saving chat messages for project {validated_project_id}:")
                    print(f"   Error code: {error_code}")
                    print(f"   Error message: {error_msg}")
                    print(f"   Hint: {error_hint}")
                    if "row-level security" in error_msg.lower() or "rls" in error_msg.lower():
                        print(f"   ⚠️  RLS POLICY ISSUE DETECTED!")
                        print(f"   The insert is being blocked by Row Level Security policies.")
                        print(f"   Verify that SUPABASE_SERVICE_ROLE_KEY is the service role key (not anon key).")
                        print(f"   Service role key should bypass RLS automatically.")
                    print(f"   Full error details: {error_dict}")
                    
        except Exception as e:
            print(f"❌ Unexpected error saving chat history for project {req.projectId}: {e}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            # Don't fail the request if history save fails, but log thoroughly

        # Return both the message and operations
        return {
            "message": assistant_message,
            "operations": operations
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions (they already have proper status codes)
        raise
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error in chat endpoint: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

