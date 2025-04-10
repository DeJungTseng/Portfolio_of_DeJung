# System Architecture

## Class Diagram
```mermaid
classDiagram
    class MainExec {
        -type: str
        -model: object
        -user_id: str
        -movie_id: str
        +load_model()
        +model(user_id, gen_mov, gen_mov_id)
        +movie_recommended(movie_id)
        +movie_process()
    }

    class Window {
        -login_dialog: LoginDialog
        +__init__(theme)
        +create_widgets()
    }

    class LoginDialog {
        -username: StringVar
        -password: StringVar
        -parent: Window
        +__init__(parent, title)
        +body(master)
        +apply()
        +validate()
    }

    class AuthUtils {
        +hash_password(password)
        +verify_password(plain_password, hashed_password)
        +validate_login(username, password)
    }

    class DataSource {
        +get_user_id_pw(username)
        +get_watched(user_id)
        +get_user_genres(user_id)
        +genres_process(preferences)
        +get_movies()
        +get_movie_by_id(movie_id)
    }

    Window --> LoginDialog : creates
    LoginDialog --> AuthUtils : uses
    AuthUtils --> DataSource : uses
    MainExec --> DataSource : uses
    MainExec --> Window : creates

```

## Data Flow Diagram
```mermaid
flowchart TD
    subgraph User Interface
        UI[Window]
        LD[LoginDialog]
    end

    subgraph Authentication
        AU[AuthUtils]
        DB[(PostgreSQL DB)]
    end

    subgraph Recommendation Engine
        ME[MainExec]
        ML[ML Model]
    end

    subgraph Data Layer
        DS[DataSource]
    end

    User((User)) -->|Login| UI
    UI -->|Creates| LD
    LD -->|Validate| AU
    AU -->|Query| DS
    DS -->|Fetch| DB
    DB -->|Return| DS
    DS -->|Return| AU
    AU -->|Result| LD
    LD -->|Success| UI
    UI -->|Create| ME
    ME -->|Load| ML
    ME -->|Query| DS
    DS -->|Movie Data| ME
    ME -->|Recommendations| UI
    UI -->|Display| User
```

## Component Descriptions

### User Interface Layer
- **Window**: Main application window using tkinter
- **LoginDialog**: Handles user authentication UI

### Authentication Layer
- **AuthUtils**: Manages password hashing and verification
- **Database**: Stores user credentials and movie data

### Recommendation Engine
- **MainExec**: Core recommendation logic
- **ML Model**: Machine learning model for recommendations

### Data Layer
- **DataSource**: Database access and data processing

## Data Flow Process

1. **Login Flow**:
   - User enters credentials
   - LoginDialog passes to AuthUtils
   - AuthUtils verifies with DataSource
   - DataSource queries PostgreSQL
   - Result flows back to UI

2. **Recommendation Flow**:
   - MainExec loads ML model
   - Queries user preferences via DataSource
   - Processes recommendations
   - Returns results to Window
   - Window displays to user

## Security Features
- Passwords are hashed using bcrypt
- Salt is automatically generated per password
- No plain text passwords stored in database
