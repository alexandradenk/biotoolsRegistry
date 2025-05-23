# --------------- GENERAL ---------------

INVALID = "invalid"
VALID = "valid"
STRING = "string"
ARRAY = "array"
OBJECT = "object"

DEFINITIONS = "definitions"
PROPERTIES = "properties"
ITEMS = "items"
TOOL = "tool"
REF = "$ref"
TYPE = "type"

# --------- DICTIONARY TEMPLATES --------

VALUE_DICT_BASE = {VALID: [], INVALID: []}

TYPE_DICT = {  # data types and constraints (e.g. "string": ["minLength", "pattern"]
    STRING: ["minLength", "maxLength", "enum", "pattern", "anyOf", "examples"],
    ARRAY: ["minItems", "maxItems"]
}

# ---------- STRING ATTRIBUTES ----------

MIN_LENGTH = "minLength"
MAX_LENGTH = "maxLength"
ENUM = "enum"
PATTERN = "pattern"
ANY_OF = "anyOf"
EXAMPLES = "examples"

# ------------ STRING VALUES ------------

DEFAULT_BASE_STRING = "TEST"
EMPTY_STRING = ""

# ----------- ARRAY ATTRIBUTES ----------

MIN_ITEMS = "minItems"
MAX_ITEMS = "maxItems"
