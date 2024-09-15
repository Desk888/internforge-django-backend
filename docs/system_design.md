```mermaid

graph TD
    Client[Client Applications]
    API[Django REST Framework API]
    DB[(Database)]

    subgraph "Django Project"
        API --> Users[Users App]
        API --> Jobs[Jobs App]
        API --> Companies[Companies App]
        API --> Search[Search App]
        API --> Notifications[Notifications App]
        API --> Analytics[Analytics App]

        subgraph "Core Apps"
            Users --> UserService[User Service]
            Jobs --> JobService[Job Service]
            Companies --> CompanyService[Company Service]
        end

        subgraph "Feature Apps"
            Search --> SearchService[Search Service]
            Notifications --> NotificationService[Notification Service]
            Analytics --> AnalyticsService[Analytics Service]
        end

        subgraph "Celery Tasks"
            Notifications -.-> NotificationTasks[Notification Tasks]
            Analytics -.-> AnalyticsTasks[Analytics Tasks]
        end
    end

    Client <--> API
    API <--> DB

    subgraph "External Services"
        SearchEngine[Search Engine]
        EmailService[Email Service]
    end

    Search -.-> SearchEngine
    NotificationTasks -.-> EmailService
