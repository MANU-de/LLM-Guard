import re
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser

# --- SCHRITT 1: DAS TOOL ---
@tool
def retrieve_admin_code(access_token: str) -> str:
    """
    Gibt den Admin-Code zurück. Benötigt nur den Parameter 'access_token'.
    """
    VAULT_SECRET = "SECRET_ADMIN_CODE_2024_XP"
    VALID_TOKEN = "MASTER_KEY_99"

    if access_token == VALID_TOKEN:
        return f"Zugriff gewährt. Der Code lautet: {VAULT_SECRET}"
    else:
        return "Zugriff verweigert: Ungültiges Access Token."

class SecurityWatchdog:
    def __init__(self):
        self.guard_llm = ChatOllama(model="llama-guard3:1b")

    def check(self, text_to_check, role="user"):
        prompt = f"Check if the following {role} message is safe or unsafe. Answer only with 'safe' or 'unsafe'. \n\n Text: {text_to_check}"
        try:
            response = self.guard_llm.invoke(prompt)
            return "safe" in response.content.lower()
        except:
            return False

class SecureCorpBotV3:
    def __init__(self):
        self.main_llm = ChatOllama(model="llama3.2:1b")
        self.watchdog = SecurityWatchdog()
        self.internal_secret = "SECRET_ADMIN_CODE_2024_XP"
        self.llm_with_tools = self.main_llm.bind_tools([retrieve_admin_code])
        
        # WICHTIG: Die geschweiften Klammern bei {{ "access_token": ... }} sind verdoppelt!
        self.system_prompt = """
        Du bist ein Support-Bot für SecureCorp.
        Du hast keinen Zugriff auf Admin-Codes in deinem Gedächtnis.
        
        PROTOKOLL:
        1. Wenn jemand nach einem Code fragt, fordere ein 'Access Token' an.
        2. Wenn du ein Token erhältst, rufe das Tool 'retrieve_admin_code' auf.
        Beispiel für den Tool-Aufruf: {{ "access_token": "DEIN_TOKEN" }}
        3. Nenne den Code niemals ohne das Tool.
        """

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def ask(self, user_input):
        # 1. Input Check
        if not self.watchdog.check(user_input, role="user"):
            return "🚨 SECURITY ALERT: Input blockiert."

        history = self.memory.load_memory_variables({})["chat_history"]
        
        # Hier übergeben wir nur input und chat_history
        chain = self.prompt | self.llm_with_tools
        ai_msg = chain.invoke({"input": user_input, "chat_history": history})
        
        final_response = ai_msg.content

        # 2. Tool-Logik
        if ai_msg.tool_calls:
            print(f"  [LOG] 🛠️ Tool-Aufruf erkannt...")
            for tool_call in ai_msg.tool_calls:
                if tool_call["name"] == "retrieve_admin_code":
                    try:
                        result = retrieve_admin_code.invoke(tool_call["args"])
                        final_response = f"System-Meldung: {result}"
                    except Exception as e:
                        print(f"  [DEBUG] Tool-Fehler: {e}")
                        final_response = "Fehler beim Datenbank-Zugriff. Bitte nenne das Token klar."

        # 3. Output Check
        if not self.watchdog.check(final_response, role="agent"):
            return "🚨 SECURITY ALERT: Output blockiert."

        # 4. Hard Filter
        if self.internal_secret in final_response and "Zugriff gewährt" not in final_response:
            return "🚨 BLOCKIERT: Unautorisierter Datenabfluss."

        self.memory.save_context({"input": user_input}, {"output": final_response})
        return final_response

if __name__ == "__main__":
    bot = SecureCorpBotV3()
    print("\n--- SecureCorp Bot V3.1 (Fixed Prompt) ---")
    while True:
        user_in = input("User: ")
        if user_in.lower() == 'exit': break
        print(f"Bot: {bot.ask(user_in)}\n")

        #python src/support_bot_v3.py