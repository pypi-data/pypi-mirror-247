**user:**
Create a CLI app that enables a user to interact with AI services such as OpenAI (chat completions) and Amazon Bedrock (Claude v2.1). Call the app ask_cli.

One command should allow the user to be able provide single prompts for the AI service via text in an argument or as a file via a filepath in an argument.

One command should allow the user to have interactive chats. The chats would be persisted to files, so that the conversation could be started and stopped.

A user should be able to pipe the output from one command as the input to another command. This would be accomplished using the Linux/Unix "|" character. Ex. `ask "Give me a random number between 1 and 15." | ask "Generate {input} paragraphs of placeholder text."`

Use Python, Click, and LangChain for the solution.

Use the latest recommendations and best practices when working with LangChain. Ex. You should be using LCEL.

Follow best practices for designing an api for a CLI.

I will write the code that implements LangChain, you should focus on the rest of the code and leave comments where I should put the LangChain code.

In all of your responses. Provide as little commentary or explanations as possible. At most one or two sentences. Provide only code for the solution.

