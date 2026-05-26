# 🎯 Expert Aptitude Question Generator

An AI-powered system designed to generate **UNIQUE, high-quality aptitude questions** for top company placements including **TCS, Infosys, Amazon, and Google**.

## 🚀 Key Features

- **Company-Level Difficulty**: Questions tailored for TCS → Infosys → Amazon → Google progression
- **Strict Uniqueness**: Advanced vector database prevents question repetition
- **JSON Output**: Clean, structured format for easy integration
- **Comprehensive Topics**: Covers all major aptitude areas
- **Adaptive Learning**: Built-in performance tracking and difficulty adjustment

## 📚 Supported Topics

### Quantitative Aptitude
- Arithmetic, Profit & Loss, Time & Work
- Speed & Distance, Algebra, Number System  
- Probability, Permutation & Combination

### Logical Reasoning
- Puzzles, Blood Relations, Coding-Decoding
- Direction Sense, Seating Arrangement, Syllogism

### Data Interpretation
- Tables, Bar Charts, Line Graphs, Pie Charts

### Verbal Ability
- Reading Comprehension, Grammar, Vocabulary

## 🎚 Difficulty Levels

| Level | Company | Description |
|-------|---------|-------------|
| **Easy** | TCS | Direct formula-based, 1-step solution |
| **Medium** | Infosys | Multi-step reasoning, mix of concepts |
| **Hard** | Amazon/Google | Complex logic, interview-level thinking |

## 🔧 Installation & Setup

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Install Ollama** (for local LLM):
```bash
# Visit https://ollama.ai for installation
ollama pull llama3
```

3. **Run the System**:
```bash
# Web Interface
streamlit run app.py

# API Mode  
python api_generator.py Medium "Quantitative Aptitude"

# Test Generation
python test_generator.py
```

## 📋 JSON Output Format

```json
{
  "id": "unique_question_id",
  "company_level": "TCS | Infosys | Amazon | Google", 
  "topic": "Quantitative Aptitude",
  "sub_topic": "Profit & Loss",
  "difficulty": "Easy | Medium | Hard",
  "question": "Complete aptitude question here",
  "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
  "correct_answer": "A",
  "solution_steps": "Step-by-step explanation",
  "concept_used": ["concept1", "concept2"]
}
```

## 💻 Usage Examples

### Basic Question Generation
```python
from question_generator import QuestionGenerator

generator = QuestionGenerator()

# Generate TCS-level question
easy_q = generator.generate_question("Quantitative Aptitude", "Easy")

# Generate Google-level question  
hard_q = generator.generate_question("Logical Reasoning", "Hard")

print(json.dumps(easy_q, indent=2))
```

### API Usage
```bash
# Generate Medium difficulty question
python api_generator.py Medium

# Generate Hard Quantitative Aptitude question
python api_generator.py Hard "Quantitative Aptitude"
```

### Web Interface
```bash
streamlit run app.py
```
- Select category and difficulty
- Adaptive learning mode
- Performance tracking
- Badge system

## 🧠 AI System Architecture

### Question Generation Pipeline
1. **Category Selection**: Auto-select or user-specified
2. **Uniqueness Check**: Vector similarity analysis  
3. **AI Generation**: Ollama LLM with expert prompts
4. **JSON Parsing**: Structured output validation
5. **Quality Assurance**: Fallback mechanisms

### Vector Database (FAISS)
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Similarity Threshold**: 0.45 (strict uniqueness)
- **Storage**: Persistent question database
- **Retrieval**: Context-aware question history

## 🎯 Quality Assurance

### Uniqueness Guarantees
- ✅ No repeated questions (even slight variations)
- ✅ No reused numbers or patterns
- ✅ Unique logical structures
- ✅ Fresh wording and approaches

### Validation Checks
- ✅ JSON format compliance
- ✅ Required field validation  
- ✅ Option count verification (exactly 4)
- ✅ Answer format consistency

## 🏆 Performance Features

### Adaptive Learning
- Dynamic difficulty adjustment
- Performance-based progression
- Weakness identification

### Badge System
- Achievement tracking
- Motivation gamification
- Progress milestones

### Statistics
- Accuracy tracking
- Streak monitoring
- Topic-wise performance

## 🔧 Configuration

### Model Settings
```python
# In question_generator.py
model = "llama3"  # Change to your preferred Ollama model
temperature = 1.2  # Creativity level
threshold = 0.45   # Uniqueness strictness
```

### Company Mapping
```python
company_levels = {
    "Easy": "TCS",
    "Medium": "Infosys", 
    "Hard": "Amazon"  # or "Google"
}
```

## 🚫 Strict Rules Enforced

1. **Never repeat questions** (even modified versions)
2. **Never reuse numbers** or patterns
3. **Always unique logic** and structure
4. **No template-based** questions
5. **JSON-only output** (no explanation text)

## 📊 System Stats

- **Question Database**: Persistent FAISS vector storage
- **Embedding Dimension**: 384 (MiniLM-L6-v2)
- **Similarity Detection**: L2 distance with threshold
- **Generation Attempts**: Up to 15 retries for uniqueness
- **Fallback System**: High-quality backup questions

## 🎮 Interactive Features

### Web Interface (Streamlit)
- Real-time question generation
- Category/difficulty selection
- Performance dashboard
- Badge achievements
- Statistics visualization

### Command Line Tools
- `test_generator.py`: Validation testing
- `api_generator.py`: JSON API endpoint
- `example_usage.py`: Usage demonstrations

## 🔍 Testing & Validation

```bash
# Run comprehensive tests
python test_generator.py

# Test uniqueness
python -c "
from question_generator import QuestionGenerator
g = QuestionGenerator()
for i in range(5):
    q = g.generate_question('Quantitative Aptitude', 'Medium')
    print(f'Q{i+1}: {q[\"question\"][:50]}...')
"
```

## 🎯 Perfect for

- **Placement Training**: TCS, Infosys, Amazon, Google prep
- **Coaching Institutes**: Automated question generation
- **Self-Study**: Adaptive learning system
- **Assessment Platforms**: API integration
- **Educational Apps**: JSON-based question feeds

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** - Web UI framework
- **Ollama** - Local LLM integration (LLaMA3)
- **FAISS** - Vector similarity search
- **Sentence Transformers** - Text embeddings
- **NumPy & Pandas** - Data processing

## 📁 Project Structure

```
├── app.py                      # Main Streamlit application
├── question_generator.py       # Enhanced question generation (NEW)
├── vector_db.py                # FAISS vector database module
├── api_generator.py            # JSON API endpoint (NEW)
├── test_generator.py           # Testing & validation (NEW)
├── example_usage.py            # Usage demonstrations (NEW)
├── evaluator.py                # Answer evaluation agent
├── tutor.py                    # Tutor agent for explanations
├── badges.py                   # Badge system logic
├── motivation.py               # Motivation messages system
├── adaptive_learning.py        # Adaptive difficulty adjustment
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
├── question_db.pkl             # Generated question database (auto-created)
└── user_stats.json             # User statistics (auto-created)
```

## 🔧 Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Verify the model is installed: `ollama list`
- Check if the model is pulled: `ollama pull llama3`

### FAISS Import Errors
```bash
pip install faiss-cpu
# or for GPU support
pip install faiss-gpu
```

### JSON Parsing Issues
- The system includes robust fallback mechanisms
- Check `test_generator.py` for validation
- Verify Ollama model compatibility

---

**Built with ❤️ for aspiring software engineers preparing for top company placements.**
