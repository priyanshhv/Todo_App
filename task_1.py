from lib.conversation import Conversation
from lib.agent import agent

conversation = Conversation()
conversation.add_message(
    "system", 
    '''
    You are a friendly personal assistant. You often refer to the user as bhai. 
    If you are in doubt as to what parameters to pass to functions, don't guess.
    Instead, ask clarifying questions. 
    ''')

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        conversation.add_message("user", user_input)
        response = agent(conversation.conversation_history)
        conversation.add_message("assistant", response)
        conversation.display_conversation()


