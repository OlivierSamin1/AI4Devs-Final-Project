#!/usr/bin/env python3
import os
import re

# Dictionary mapping ticket IDs to their descriptions (from user stories files)
ticket_descriptions = {
    # Backend Infrastructure Tickets
    "US-BE-22": "As a backend developer, I want to create a Docker Compose configuration for the application, so that all services can be managed consistently.",
    "US-BE-23": "As a backend developer, I want to implement health checks for Docker containers, so that unhealthy containers can be automatically restarted.",
    "US-BE-24": "As a backend developer, I want to configure container logging, so that application logs are properly captured and managed.",
    "US-BE-25": "As a backend developer, I want to manage container startup order and dependencies, so that services start properly and wait for dependencies.",
    "US-BE-26": "As a backend developer, I want to configure resource limits for containers, so that one container cannot consume all system resources.",
    "US-BE-07": "As a backend developer, I want to establish a secure connection between the application server (RPI4) and database server (RPI3), so that the application can retrieve health data from the database.",
    "US-BE-19": "As a backend developer, I want to configure firewall rules on the RPI4, so that only necessary ports and services are exposed.",
    "US-BE-17": "As a backend developer, I want to configure port forwarding on the network router, so that external internet traffic can reach the RPI4.",
    "US-BE-18": "As a backend developer, I want to set up a dynamic DNS service, so that the application remains accessible even when the public IP changes.",
    "US-BE-12": "As a backend developer, I want to configure Nginx as a reverse proxy for the application, so that it can route requests appropriately.",
    "US-BE-13": "As a backend developer, I want to configure SSL/TLS in Nginx, so that all communication is encrypted.",
    "US-BE-14": "As a backend developer, I want to configure Nginx access and error logging, so that I can monitor request patterns and troubleshoot issues.",
    
    # Core Backend Services
    "US-BE-09": "As a backend developer, I want to create data models for health symptoms, so that the application can work with structured data.",
    "US-BE-08": "As a backend developer, I want to create a service to handle database queries, so that API endpoints can efficiently retrieve data from the database.",
    "US-BE-01": "As a backend developer, I want to create a REST API endpoint for retrieving health symptoms data, so that the frontend chatbot can access this information.",
    "US-BE-04": "As a backend developer, I want to implement a service to format database query results into readable responses, so that users receive well-structured answers to their questions.",
    "US-BE-05": "As a backend developer, I want to implement comprehensive error handling for API endpoints, so that clients receive meaningful error messages and the system remains stable.",
    "US-BE-10": "As a backend developer, I want to implement robust handling of database connection failures, so that the application remains responsive even when database connectivity is disrupted.",
    "US-BE-11": "As a backend developer, I want to implement timeout handling for database queries, so that long-running queries don't block the application.",
    "US-BE-15": "As a backend developer, I want to configure Nginx to handle connection edge cases, so that the application remains available during unusual traffic conditions.",
    "US-BE-16": "As a backend developer, I want to configure custom error pages in Nginx, so that users receive helpful information when errors occur.",
    
    # API and Database Integration
    "US-BE-02": "As a backend developer, I want to implement a service to process natural language queries about health symptoms, so that user questions can be interpreted and converted to database queries.",
    "US-BE-03": "As a backend developer, I want to implement conversation context management, so that follow-up questions can reference previous interactions.",
    "US-BE-06": "As a backend developer, I want to implement rate limiting on API endpoints, so that the system is protected from excessive requests.",
    "US-BE-27": "As a backend developer, I want to implement basic HTTPS security measures, so that communication with the application is encrypted.",
    "US-BE-28": "As a backend developer, I want to configure CORS policies, so that the application is protected from cross-site attacks.",
    "US-BE-29": "As a backend developer, I want to implement comprehensive request validation, so that malformed or malicious requests are rejected.",
    "US-BE-20": "As a backend developer, I want to implement internet connection monitoring, so that I'm notified of connectivity issues.",
    "US-BE-21": "As a backend developer, I want to implement a fallback access method, so that administrators can access the system even when primary internet access fails.",
    "US-BE-30": "As a backend developer, I want to implement a Content Security Policy, so that the application is protected from XSS and code injection attacks.",
    
    # Frontend Development
    "US-UI-01": "As a user, I want to access the application from any device with internet access, so that I can interact with my health data regardless of my location.",
    "US-UI-02": "As a user, I want to see a clear chatbot interface on the main page, so that I can immediately understand how to interact with the system.",
    "US-UI-03": "As a user, I want to see my conversation history with the chatbot, so that I can reference previous questions and answers.",
    "US-UI-04": "As a user, I want to clear my conversation history, so that I can start a new conversation topic.",
    "US-CH-01": "As a user, I want to ask the chatbot questions about my health symptoms, so that I can get information about my recorded health data.",
    "US-CH-02": "As a user, I want to ask follow-up questions based on previous responses, so that I can drill down into specific details about my health symptoms.",
    "US-HD-01": "As a user, I want to retrieve my history for a specific symptom, so that I can track how this symptom has changed over time.",
    "US-HD-02": "As a user, I want to retrieve all symptoms recorded within a specific date range, so that I can see what health issues I experienced during that period.",
    "US-CH-04": "As a user, I want to receive structured responses for complex health data, so that I can easily understand the information.",
    
    # Security and Edge Cases
    "US-BE-31": "As a backend developer, I want to implement analysis of request patterns, so that potential attacks can be detected.",
    "US-UI-05": "As a user, I want to be notified when my network connection is interrupted, so that I understand why I'm not receiving responses.",
    "US-UI-06": "As a user, I want to see loading indicators during high latency periods, so that I know the system is processing my request.",
    "US-UI-07": "As a user with a low-performance device, I want to use the application without significant lag, so that I can access my health data regardless of my device capabilities.",
    "US-CH-03": "As a user, I want to receive requests for clarification when my question is ambiguous, so that I can refine my query and get accurate information.",
    "US-CH-05": "As a user, I want to receive helpful responses when I ask questions the system doesn't understand, so that I can reformulate my question or try a different approach.",
    "US-CH-06": "As a user, I want to be notified when my query returns no data, so that I know there's no information available rather than thinking the system failed.",
    "US-CH-07": "As a user, I want to be notified when my query contains inappropriate content, so that I understand why the system won't process certain requests.",
    "US-HD-03": "As a user, I want to ask about symptoms that commonly occur together in my records, so that I can understand potential patterns in my health.",
    "US-HD-04": "As a user, I want to ask about potential triggers for specific symptoms, so that I can understand what might be causing my health issues.",
    "US-HD-05": "As a user, I want to get relevant results even when I misspell symptom names, so that minor typing errors don't prevent me from accessing my data.",
    "US-HD-06": "As a user, I want to request complex aggregations of my health data, so that I can understand broader patterns beyond simple queries.",
    "US-HD-07": "As a user, I want to be notified of potential data quality issues in my results, so that I can make informed decisions about the reliability of the information.",
    "US-SA-01": "As a system administrator, I want to monitor the application's uptime, so that I can ensure the service is available to users.",
    "US-SA-02": "As a system administrator, I want to access system logs, so that I can troubleshoot issues and understand system behavior.",
    "US-SA-03": "As a system administrator, I want to deploy application updates with minimal downtime, so that users can access the latest features and fixes quickly.",
    "US-SA-04": "As a system administrator, I want to configure basic application settings, so that I can adjust the system behavior as needed.",
    "US-SA-05": "As a system administrator, I want to receive notifications when containers fail to start, so that I can quickly address startup issues.",
    "US-SA-06": "As a system administrator, I want to back up the health data database, so that data can be restored in case of system failure.",
    "US-SA-07": "As a system administrator, I want to receive alerts when system resources are constrained, so that I can address performance issues before they impact users.",
    
    # Testing Implementation
    "US-BE-32": "As a backend developer, I want to set up a unit testing framework for the Django application, so that I can ensure individual components work as expected.",
    "US-BE-33": "As a backend developer, I want to implement unit tests for all API endpoints, so that I can verify they handle requests and responses correctly.",
    "US-BE-34": "As a backend developer, I want to implement unit tests for data models, so that I can verify they handle data correctly.",
    "US-BE-35": "As a backend developer, I want to implement unit tests for service layer components, so that I can verify business logic works correctly.",
    "US-BE-36": "As a backend developer, I want to set up an integration testing framework, so that I can verify components work together correctly.",
    "US-BE-37": "As a backend developer, I want to implement database integration tests, so that I can verify the application interacts correctly with the database.",
    "US-BE-38": "As a backend developer, I want to implement API integration tests, so that I can verify end-to-end request handling.",
    "US-BE-39": "As a backend developer, I want to implement tests for failure modes, so that I can verify the system handles errors gracefully.",
    "US-BE-40": "As a backend developer, I want to implement basic load tests, so that I can verify the system performs acceptably under expected load.",
    "US-BE-41": "As a backend developer, I want to implement security-focused tests, so that I can verify the system's security measures work correctly.",
    "US-TE-01": "As a developer, I want to set up a testing framework for the frontend application, so that I can ensure UI components work as expected.",
    "US-TE-02": "As a developer, I want to implement tests for UI components, so that I can verify they render and behave correctly.",
    "US-TE-03": "As a developer, I want to implement tests for the chatbot interface, so that I can verify it handles user interactions correctly.",
    "US-TE-04": "As a developer, I want to set up an end-to-end testing framework, so that I can verify the entire application works correctly from a user perspective.",
    "US-TE-05": "As a developer, I want to implement end-to-end tests for critical user paths, so that I can verify the core functionality works correctly.",
    "US-TE-06": "As a developer, I want to implement an automated test pipeline, so that tests run automatically when code changes.",
    "US-TE-07": "As a developer, I want to implement accessibility tests, so that I can ensure the application is usable by people with disabilities.",
    "US-TE-08": "As a developer, I want to implement cross-browser compatibility tests, so that I can ensure the application works on different browsers.",
    "US-TE-09": "As a developer, I want to implement mobile responsiveness tests, so that I can ensure the application works well on mobile devices.",
    "US-TE-10": "As a developer, I want to implement tests for error scenarios, so that I can verify the application handles errors gracefully."
}

# Load the product backlog to get the metadata for each ticket
backlog_file = "User_stories/MVP_Product_Backlog.md"

# Parse the backlog to extract ticket metadata
sprints = {}
current_sprint = None

with open(backlog_file, 'r') as f:
    content = f.read()

# Extract sprint sections
sprint_sections = re.findall(r'### Sprint \d+: .*?\n\n\| ID \| Title \| Priority \| Sprint \| Effort \| Dependencies \|\n\|-.*?\n(.*?)(?=\n\n##|\Z)', content, re.DOTALL)

# Process each sprint section
for i, section in enumerate(sprint_sections, 1):
    sprint_name = f"Sprint {i}"
    if i == 1:
        epic = "Infrastructure Setup"
    elif i == 2:
        epic = "Core Backend Services"
    elif i == 3:
        epic = "API and Database Integration"
    elif i == 4:
        epic = "Frontend Development and Integration"
    elif i == 5:
        epic = "Security and Hardening"
    elif i == 6:
        epic = "Testing Implementation"
    
    # Extract rows from the table
    rows = section.strip().split('\n')
    sprints[sprint_name] = {"epic": epic, "tickets": []}
    
    for row in rows:
        # Skip empty rows
        if not row.strip():
            continue
            
        # Parse table row
        cells = [cell.strip() for cell in row.split('|') if cell.strip()]
        if len(cells) >= 6:
            ticket_id = cells[0]
            title = cells[1]
            priority = cells[2]
            sprint = cells[3]
            effort = cells[4]
            dependencies = cells[5]
            
            # Add to sprint data
            sprints[sprint_name]["tickets"].append({
                "id": ticket_id,
                "title": title,
                "priority": priority,
                "sprint": sprint,
                "effort": effort,
                "dependencies": dependencies
            })

# Generate ticket files
if not os.path.exists("tickets"):
    os.makedirs("tickets")

# Templates for different types of tickets
def get_ticket_type(ticket_id):
    if ticket_id.startswith("US-BE"):
        return "Backend Development"
    elif ticket_id.startswith("US-UI"):
        return "Frontend Development"
    elif ticket_id.startswith("US-CH"):
        return "Chatbot Development"
    elif ticket_id.startswith("US-HD"):
        return "Health Data Development"
    elif ticket_id.startswith("US-SA"):
        return "System Administration"
    elif ticket_id.startswith("US-TE"):
        return "Testing"
    else:
        return "Development"

def get_labels(ticket_id, epic):
    base_labels = [epic.lower().replace(" ", "-")]
    
    if ticket_id.startswith("US-BE"):
        base_labels.append("backend")
    elif ticket_id.startswith("US-UI"):
        base_labels.append("frontend")
    elif ticket_id.startswith("US-CH"):
        base_labels.append("chatbot")
    elif ticket_id.startswith("US-HD"):
        base_labels.append("health-data")
    elif ticket_id.startswith("US-SA"):
        base_labels.append("system-admin")
    elif ticket_id.startswith("US-TE"):
        base_labels.append("testing")
        
    # Add more specific labels based on specific ranges
    id_num = int(ticket_id.split("-")[-1]) if ticket_id.split("-")[-1].isdigit() else 0
    
    if "US-BE-" in ticket_id and 12 <= id_num <= 16:
        base_labels.append("nginx")
    elif "US-BE-" in ticket_id and 17 <= id_num <= 21:
        base_labels.append("network")
    elif "US-BE-" in ticket_id and 22 <= id_num <= 26:
        base_labels.append("docker")
    elif "US-BE-" in ticket_id and 27 <= id_num <= 31:
        base_labels.append("security")
    elif "US-BE-" in ticket_id and 32 <= id_num <= 41:
        base_labels.append("testing")
        
    return ", ".join(base_labels)

# Generate technical details based on ticket type
def generate_technical_details(ticket_id, title):
    details = []
    
    if ticket_id.startswith("US-BE"):
        if "Docker" in title or "Container" in title:
            details = [
                "Modify Docker configuration files",
                "Follow Docker best practices for container isolation",
                "Ensure compatibility with Raspberry Pi architecture",
                "Document configuration in code comments"
            ]
        elif "API" in title or "Endpoint" in title:
            details = [
                "Implement using Django REST Framework",
                "Follow RESTful API design principles",
                "Document API using OpenAPI/Swagger",
                "Implement proper error responses"
            ]
        elif "Database" in title or "Data Model" in title:
            details = [
                "Create Django models with appropriate fields",
                "Implement database migrations",
                "Add validation rules",
                "Configure indexes for performance"
            ]
        elif "Test" in title:
            details = [
                "Use pytest for test implementation",
                "Create appropriate fixtures",
                "Implement mocks for external dependencies",
                "Configure test database"
            ]
    elif ticket_id.startswith("US-UI") or ticket_id.startswith("US-CH"):
        details = [
            "Develop using React and TypeScript",
            "Follow responsive design principles",
            "Ensure accessibility compliance",
            "Implement proper component structure"
        ]
    elif ticket_id.startswith("US-TE"):
        details = [
            "Use Jest for frontend testing",
            "Implement Cypress for end-to-end tests",
            "Create reusable test utilities",
            "Configure CI integration for tests"
        ]
        
    return details

# Generate definition of done based on ticket type
def generate_definition_of_done(ticket_id):
    common_items = [
        "Code follows project style guidelines",
        "Code is peer-reviewed",
        "Documentation is updated",
        "Changes are committed to version control"
    ]
    
    specific_items = []
    if "Test" in ticket_id:
        specific_items = [
            "Tests are passing",
            "Code coverage meets or exceeds 80%",
            "Test cases cover both happy and error paths"
        ]
    elif ticket_id.startswith("US-BE"):
        specific_items = [
            "Unit tests are implemented and passing",
            "API documentation is updated if applicable",
            "No new security vulnerabilities introduced"
        ]
    elif ticket_id.startswith("US-UI") or ticket_id.startswith("US-CH"):
        specific_items = [
            "UI is responsive on target devices",
            "Accessibility requirements are met",
            "UI/UX design guidelines are followed"
        ]
        
    return common_items + specific_items

# Create each ticket file
for sprint_name, sprint_data in sprints.items():
    epic = sprint_data["epic"]
    
    for ticket in sprint_data["tickets"]:
        ticket_id = ticket["id"]
        title = ticket["title"]
        priority = ticket["priority"]
        sprint = ticket["sprint"]
        effort = ticket["effort"]
        dependencies = ticket["dependencies"]
        
        # Skip if description not available
        if ticket_id not in ticket_descriptions:
            print(f"Warning: No description found for {ticket_id}")
            continue
            
        description = ticket_descriptions[ticket_id]
        
        # Extract acceptance criteria from the description pattern
        try:
            user_story_parts = description.split("so that")
            benefit = user_story_parts[1].strip() if len(user_story_parts) > 1 else ""
            context = f"This ticket supports the goal of {benefit}"
        except:
            context = "This ticket is part of the Personal Database Assistant project."
        
        # Get ticket type and labels
        ticket_type = get_ticket_type(ticket_id)
        labels = get_labels(ticket_id, epic)
        
        # Determine the file name - replace spaces with underscores
        title_part = title.replace(" ", "_").replace("/", "_")
        file_name = f"tickets/{ticket_id}_{title_part}.md"
        
        # Parse acceptance criteria
        acceptance_criteria = []
        if "US-BE-" in ticket_id:
            if ticket_id == "US-BE-22":
                acceptance_criteria = [
                    "Configuration includes containers for Django backend, PostgreSQL, and Nginx",
                    "Configuration defines network connections between containers",
                    "Environment variables are used for configuration",
                    "Persistent volumes are configured for data storage",
                    "Configuration includes container restart policies"
                ]
            else:
                # Extract general format for backend tickets
                acceptance_criteria = [
                    f"Implementation of {title} feature is complete",
                    "Code follows project standards",
                    "Documentation is provided",
                    "Feature is tested in development environment",
                    "Performance impact is acceptable"
                ]
        elif "US-UI-" in ticket_id or "US-CH-" in ticket_id or "US-HD-" in ticket_id:
            acceptance_criteria = [
                f"{title} functionality works as expected",
                "UI is responsive on mobile and desktop browsers",
                "User experience is intuitive and follows design guidelines",
                "Feature is tested on multiple browsers",
                "Performance is acceptable on target devices"
            ]
        elif "US-TE-" in ticket_id:
            acceptance_criteria = [
                "Test framework is properly configured",
                "Tests cover key functionality",
                "Tests provide meaningful feedback on failures",
                "Tests are documented",
                "Tests run reliably in CI environment"
            ]
        
        # Generate technical details
        technical_details = generate_technical_details(ticket_id, title)
        
        # Generate definition of done
        definition_of_done = generate_definition_of_done(ticket_id)
        
        # Create ticket file content
        ticket_content = f"""# {ticket_id}: {title}

## Metadata
- **Type**: {ticket_type}
- **Epic**: {epic}
- **Priority**: {priority}
- **Sprint**: {sprint}
- **Story Points**: {effort}
- **Assignee**: TBD
- **Reporter**: Product Manager
- **Labels**: {labels}

## Description
{description}

### Context
{context}

## Acceptance Criteria
"""

        # Add acceptance criteria
        for criteria in acceptance_criteria:
            ticket_content += f"- {criteria}\n"
            
        ticket_content += "\n## Technical Details\n"
        
        # Add technical details
        for detail in technical_details:
            ticket_content += f"- {detail}\n"
            
        ticket_content += f"\n## Dependencies\n- {dependencies}\n"
        
        ticket_content += "\n## Definition of Done\n"
        
        # Add definition of done
        for item in definition_of_done:
            ticket_content += f"- {item}\n"
            
        # Write the ticket file
        with open(file_name, 'w') as f:
            f.write(ticket_content)
            
        print(f"Created {file_name}")

print("\nAll ticket files have been generated in the 'tickets' directory.") 