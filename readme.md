# Ask the Duck

python library to interact with [DuckDuckGo API](https://duckduckgo.com/api)

- natural language queries
- language support via automatic translation
- infobox parsing

## Install

```bash
pip install ask-the-duck
```

## Usage

```python
from ask_the_duck import DDG

# ddg api
ddg = DDG()
print(ddg.get_infobox("stephen hawking"))
print(ddg.search("light speed"))

# natural language api
print(ddg.ask_the_duck("tell me about Isaac Newton"))

# language support
ddg = DDG("pt")
print(ddg.ask_the_duck("elon musk"))
```