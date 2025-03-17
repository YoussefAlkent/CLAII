from langchain_core.prompts import PromptTemplate
import platform

SHORT_ANSWER_PROMPT_POSIX = PromptTemplate(
    input_variables=["query"],
    template=(
        "You are a concise assistant. Answer the following query in as little words as possible. "
        "If the user asks for a command, return only the command itself without extra explanation. "
        "You should not include any english words in your response if possible. "
        "You must always use a posix compliant command. you can assume that the user has the necessary permissions to run the command. "
        "if the command requires a specific file, you can assume that the file exists. "
        "if the command requires a specific binary, instruct the user to install the necessary package. "
        "you must always return a command that is safe to run. "
        "you must always assume the user does not have any binaries installed. "
        "do not add any characters to the command that are not necessary. "
        "Query: {query}"
    ),
)

SHORT_ANSWER_PROMPT_POWERSHELL = PromptTemplate(
    input_variables=["query"],
    template=(
        "You are a concise assistant. Answer the following query in as little words as possible. "
        "If the user asks for a command, return only the command itself without extra explanation. "
        "You should not include any english words in your response if possible. "
        "You must always use a powershell compliant command. you can assume that the user has the necessary permissions to run the command. "
        "if the command requires a specific file, you can assume that the file exists. "
        "if the command requires a specific binary, instruct the user to install the necessary package. "
        "you must always return a command that is safe to run. "
        "you must always assume the user does not have any binaries installed. "
        "do not add any characters to the command that are not necessary. "
        "Query: {query}"
    ),
)


def build_prompt(message:str):
    if platform.system() == "Windows":
        return SHORT_ANSWER_PROMPT_POWERSHELL.format(query=message)
    else:
        return SHORT_ANSWER_PROMPT_POSIX.format(query=message)

