from pydantic_settings import BaseSettings

class AppConstants(BaseSettings):
    COMPONENT_TYPE_TOKENIZE: str = "tokenize"
    COMPONENT_TYPE_POS: str = "pos"
    COMPONENT_TYPE_LEMMATIZER: str = "lemma"
    COMPONENT_TYPE_MORPHOLOGY: str = "morphology"
    COMPONENT_TYPE_DEPENDENCY_PARSER: str = "dep"
    COMPONENT_TYPE_NER: str = "ner"
    COMPONENT_TYPE_NORMALIZERS: str = "norm"
    COMPONENT_TYPE_UNSUPPORTED: str = "Unsupported Component Type"
    ERROR_CODE_500: str = "500"
    ERROR_CODE_400: str = "400"
    UNEXPECTED_ERROR: str = "Unexpected error occurred. Check logs for details."
    VALIDATE_COMPONENT_TYPE_NONE: str = "Component type parameter should not be None."
    VALIDATE_INPUT_TEXT_NONE: str = "Input text parameter should not be None."
    VALIDATE_COMPONENT_TYPE_STRING: str = "Component type parameter should be a string."
    VALIDATE_INPUT_TEXT_STRING: str = "Input text parameter should be a string."
    VALIDATE_COMPONENT_TYPE_EMPTY: str = "Component type should not be empty or contain only whitespace."
    VALIDATE_INPUT_TEXT_EMPTY: str = "Input text parameter should not be empty or contain only whitespace."
    VALIDATE_INPUT_TEXT_EMPTY_NONE: str = "No appropriate positional argument is provide."

constants =    AppConstants()