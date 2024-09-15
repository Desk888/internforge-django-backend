```mermaid
erDiagram
    USER ||--o{ APPLICATION : submits
    USER ||--o{ COMPANY : manages
    USER ||--o{ CV : uploads
    USER {
        int user_id PK
        string title
        string first_name
        string last_name
        string date_of_birth
        string email_address
        string password
        string phone_number
        string address_line_one
        string address_line_two
        string city
        string country
        string postcode
        string job_title
        string current_company
        datetime created_at
        enum user_type "New field"
        boolean is_active "New field"
        string profile_picture "New field"
        text bio "New field"
        datetime last_login "New field"
    }
    
    COMPANY ||--o{ JOB : posts
    COMPANY {
        int company_id PK
        string company_name
        string description
        string website
        string address_line_one
        string address_line_two
        string city
        string country
        string postcode
        string industry
        datetime created_at
        int user_id FK
        string logo "New field"
        int employee_count "New field"
        year founded_year "New field"
        enum company_status "New field"
    }
    
    JOB ||--o{ APPLICATION : receives
    JOB {
        int job_id PK
        int company_id FK
        string title
        string description
        string location
        enum contract_type
        string requirements
        string salary
        datetime created_at
        enum status
        date application_deadline "New field"
        int number_of_openings "New field"
        boolean is_remote "New field"
        string experience_level "New field"
    }
    
    CV ||--o{ APPLICATION : used_in
    CV {
        int cv_id PK
        int user_id FK
        string file_name
        string file_path
        datetime uploaded_at
        boolean is_active
        string version "New field"
    }
    
    APPLICATION {
        int application_id PK
        int user_id FK
        int job_id FK
        int cv_id FK
        string cover_letter
        enum status
        datetime submitted_at
        datetime last_updated "New field"
        text interviewer_notes "New field"
    }
    
    SKILL }o--o{ USER : has
    SKILL }o--o{ JOB : requires
    SKILL {
        int skill_id PK
        string name
        string description
        enum category "New field"
    }
    
    USER_SKILL {
        int user_id FK
        int skill_id FK
        int proficiency_level
        date acquired "New field"
    }
    
    JOB_SKILL {
        int job_id FK
        int skill_id FK
        boolean is_required
        int importance_level "New field"
    }
    
    NOTIFICATION {
        int notification_id PK
        int user_id FK
        boolean is_read
        datetime created_at
        string message "New field"
        enum notification_type "New field"
    }
    
    SEARCH_LOG {
        int search_log_id PK
        int user_id FK
        string query
        datetime searched_at
        int results_count "New field"
    }
