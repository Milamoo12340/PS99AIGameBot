# AI Game Bot - Pet Simulator 99 Automation System

## Overview

An intelligent game automation system designed for Pet Simulator 99 (Roblox) with advanced computer vision, reinforcement learning, and autonomous gameplay capabilities. The bot features cross-platform desktop applications, web-based dashboards, and sophisticated AI-driven automation for tasks like chest opening, egg hatching, resource collection, and zone navigation.

The system integrates multiple AI techniques including supervised/unsupervised learning, reinforcement learning (PPO, DQN, DDPG), computer vision with template matching, and autonomous pattern recognition. It provides both manual control interfaces and fully autonomous gameplay modes.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Web Dashboard (Flask-based)**
- Bootstrap 5 UI with real-time updates via JavaScript
- Multiple specialized interfaces:
  - Main dashboard (`templates/index.html`) - Command execution and quick actions
  - Item Mapper (`templates/item_mapper.html`) - Interactive game element training
  - Multi-Instance Launcher - Manages multiple game instances with mutex protection
  - PS99 Egg Hatcher - Specialized egg hatching interface
- Real-time status updates using polling (2-second intervals)
- Client-side state management for recording, learning, and automation modes

**Desktop Applications**
- Cross-platform Tkinter-based GUI (`desktop_app_cross_platform.py`)
- Native window detection and platform-specific handling (Windows/macOS/Linux)
- Alternative PyWebView implementation (`pywebview.py`) for embedded web interface
- Streamlit integration for simplified UI deployment

### Backend Architecture

**Core Automation Systems** (`core/` directory)
- **Vision System** (`vision_system.py`, `enhanced_vision_system.py`)
  - PyAutoGUI and OpenCV-based screen capture
  - Template matching for game element detection
  - Frame buffering for performance optimization
  - SerpentAI-inspired computer vision techniques (`serpent_enhanced_vision.py`)
  - D3DShot integration for ultra-fast screen capture (`d3dshot_capture.py`)

- **Automation Engine** (`automation_engine.py`)
  - PyAutoGUI-based mouse/keyboard control
  - Action queuing with worker threads
  - Human-like movement simulation
  - Safe/forbidden region definitions
  - Action history tracking with SerpentAI patterns

- **Learning Systems**
  - Basic Q-learning (`learning_system.py`)
  - Advanced RL agents: PPO (`proximal_policy_optimization.py`), DQN (`deep_q_network.py`), DDPG (`deep_deterministic_policy_gradient.py`)
  - Autonomous learning with goal-oriented improvement (`autonomous_learning_system.py`)
  - Experience replay buffers and prioritized sampling
  - Self-supervised pattern discovery

- **Macro System** (`macro_system.py`)
  - User-recorded macros with categorization (user_recorded, ai_generated, ai_learned, imported, templates)
  - AI-generated automation sequences
  - Watch-and-learn functionality for capturing user gameplay
  - Real-time action recording with PS99-specific collectors

- **Knowledge Management** (`knowledge_manager.py`)
  - Web scraping integration using Trafilatura
  - Game data aggregation from multiple sources
  - Pattern library and strategy storage
  - File-based knowledge base (JSON)

### Reinforcement Learning Architecture

**Multi-Algorithm Support**
- Proximal Policy Optimization (PPO) with clipped surrogate objectives
- Deep Q-Network (DQN) with experience replay
- Deep Deterministic Policy Gradient (DDPG) for continuous actions
- Rainbow DQN patterns from SerpentAI integration
- Generalized Advantage Estimation (GAE) for policy gradients

**Learning Components**
- Experience buffers with prioritized replay
- Q-table and neural network-based value functions
- Exploration-exploitation balancing (epsilon-greedy)
- Temporal pattern analysis and state transition tracking
- Multi-threaded learning with background optimization

### Pet Simulator 99 Specific Features

**API Integration** (`core/ps99_api_integration.py`, `core/ps99_api_collector.py`)
- Official PS99 API endpoints (pets, eggs, zones, worlds)
- Real-time data caching with 5-minute expiry
- Egg collection automation with API-driven decision making
- Pet hatching system with template detection

**Game-Specific Systems**
- Zone and world navigation (`core/ps99_zones_worlds.py`)
- Egg hatching with pet detection (`core/ps99_egg_hatcher.py`)
- Memory scanning patterns for advanced automation (`data/reference_macros.json`)
- Action recording specifically for PS99 gameplay (`core/ps99_action_recorder.py`)

### Advanced Automation Features

**Dynamic Automation Creator** (`core/dynamic_automation_creator.py`)
- Creates custom automation sequences from gameplay patterns
- Supports sequence, loop, conditional, adaptive, and parallel automation types
- Trigger-based execution (manual, timer, condition, event, performance)
- Self-modifying automation with performance optimization

**Gameplay Recording System** (`core/gameplay_recording_system.py`)
- Records complete gameplay sessions with screen context
- Analyzes action sequences for pattern extraction
- Generates optimized automation from recorded gameplay
- Performance metrics and success rate tracking

**Interactive Trainer** (`core/interactive_trainer.py`)
- User-guided training through direct interaction
- Game element mapping with visual feedback
- Zone boundary definition and safe path learning
- Item recognition training with color signatures

### Data Storage Solutions

**File-Based Storage**
- JSON files for configuration, knowledge base, macros, and learning data
- Template storage for computer vision matching
- Pickle serialization for complex Python objects (experience buffers, neural networks)

**Data Structures**
- `data/knowledge_base.json` - Scraped game information and strategies
- `data/macros.json` - Recorded automation sequences
- `data/ps99_*.json` - Pet Simulator 99 API data (eggs, pets, zones, worlds)
- `data/game_elements.json` - Detected game element definitions
- `data/learned_items.json` - AI-discovered items and patterns

### Multi-Instance Management

**Instance Coordination**
- Mutex-based protection against Roblox detection
- Shadow following system for synchronized multi-account gameplay
- Coordinated command execution across instances
- Process monitoring and automatic recovery

**Window Management** (`core/window_detector.py`)
- Cross-platform window detection (pygetwindow)
- Roblox process monitoring via psutil
- Automatic window focus and positioning
- Support for multiple concurrent game instances

### Input Capture and Playback

**Advanced Input System** (`core/advanced_input_capture.py`)
- Keyboard and mouse event recording with timestamps
- Event replay with timing preservation
- Support for complex input sequences
- Integration with macro system for automation generation

### Image Processing Pipeline

**SerpentAI Integration** (`core/serpent_image_processing.py`)
- Advanced image transformations (resize, color conversion, filtering)
- K-means clustering for color analysis
- Morphological operations and segmentation
- Jupyter notebook visualization support

### External Dependencies

**Web Framework**
- Flask 3.1.0 - Web server and API endpoints
- Flask-RESTful - RESTful API design
- Werkzeug - WSGI utilities and development server

**Computer Vision & Image Processing**
- OpenCV (opencv-python) - Core computer vision operations
- Pillow (PIL) - Image manipulation and screenshot handling
- scikit-image - Advanced image processing algorithms
- PyAutoGUI - Screen capture and GUI automation (with fallback handling)

**Machine Learning & AI**
- TensorFlow - Deep learning framework for RL agents
- PyTorch - Alternative deep learning backend
- NumPy - Numerical computations and array operations
- scikit-learn - Machine learning utilities and clustering

**Web Scraping & Data Collection**
- Trafilatura - Main content extraction from web pages
- BeautifulSoup4 (via html5lib) - HTML parsing fallback
- Requests - HTTP client for API calls
- lxml - XML/HTML processing

**Desktop Application Libraries**
- Tkinter - Cross-platform GUI framework (built-in)
- PyWebView - Embedded web browser for desktop apps
- Streamlit - Alternative dashboard framework
- pygetwindow - Window detection and management

**Game-Specific APIs**
- PS99 Official API (https://ps99.biggamesapi.io) - Pet, egg, zone, and world data
- Roblox APIs - Universe and game information (when applicable)

**Database**
- PostgreSQL (psycopg2) - Data persistence for repository analysis and knowledge storage
- Environment variables for connection configuration (PGHOST, PGPORT, PGDATABASE)

**System & Process Management**
- psutil - Process monitoring for Roblox instances
- platform - Cross-platform OS detection
- subprocess - External process execution
- threading - Concurrent operation support

**Data Formats & Serialization**
- JSON - Primary configuration and data storage format
- Pickle - Python object serialization for ML models
- HDF5 (h5py) - Large dataset storage for RL training

**Development & Utilities**
- dotenv - Environment variable management
- watchdog - File system monitoring for hot reload
- progressbar33 - Progress tracking for long operations
- Redis - Optional caching layer (configured but not required)

**Additional ML/RL Dependencies**
- Gym (OpenAI) - Reinforcement learning environments
- Roboschool - Physics-based RL environments
- datasets (Hugging Face) - Dataset management
- accelerate - Distributed training support

**System Requirements**
- Python 3.7+ with extensive ML/AI stack
- Windows/macOS/Linux support with platform-specific adaptations
- Fallback mechanisms for headless environments (mock PyAutoGUI)
- Optional GPU support for PyTorch-based RL training