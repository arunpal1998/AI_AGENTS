from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

load_dotenv()

api_key = os.getenv('google_api_key')
if not api_key:
    print('api_key not found')
    exit()

client = genai.Client(api_key=api_key)

def add(a:float,b:float):
    return a+b

def sub(a:float,b:float):
    return a-b

def mult(a:float,b:float):
    return a*b

def div(a:float,b:float):
    if b == 0:
        return 'can not divide by zero'
        
    return a/b

def flrdiv(a:float,b:float):
    if b == 0:
        return 'can not divide by zero'
    
    return a//b

def mod(a:float,b:float):
    return a%b

def powr(a:float,b:float):
    return a**b

add_tool = types.FunctionDeclaration(
    name='add',
    description='addition of two numbers',
    parameters=types.Schema(
        type = 'object',
        properties={
            'a':types.Schema(type='NUMBER'),
            'b':types.Schema(type='NUMBER')
        },
        required=['a','b']
    )
)

sub_tool = types.FunctionDeclaration(
    name='sub',
    description='subtract second number from first',
    parameters=types.Schema(
        type='object',
        properties={
            'a':types.Schema(type='NUMBER'),
            'b':types.Schema(type='NUMBER')
        },
        required=['a','b']     
    )
)

mult_tool=types.FunctionDeclaration(
    name='mult',
    description='multiplication of two numbers',
    parameters=types.Schema(
        type='object',
        properties={
            'a':types.Schema(type='NUMBER'),
            'b':types.Schema(type='NUMBER')
        },
        required=['a','b']
    )
)

div_tool = types.FunctionDeclaration(
    name='div',
    description='division of two numbers',
    parameters=types.Schema(
        type='object',
        properties={
            'a':types.Schema(type='NUMBER'),
            'b':types.Schema(type='NUMBER')
        },
        required=['a','b']
    )
)

flrdiv_tool =types.FunctionDeclaration(
    name='flrdiv',
    description='floor division of the numbers',
    parameters=types.Schema(
        type='object',
        properties={
            'a':types.Schema(type='NUMBER'),
            'b':types.Schema(type='NUMBER')
        },
        required=['a','b']
    )
)

mod_tool = types.FunctionDeclaration(
    name='mod',
    description='find the modulus for the given numbers',
    parameters=types.Schema(
        type='object',
        properties={
            'a':types.Schema(type='NUMBER'),
            'b':types.Schema(type='NUMBER')
        },
        required=['a','b']
    )
)

powr_tool = types.FunctionDeclaration(
    name='powr',
    description='calculate the power of numbers',
    parameters=types.Schema(
        type='object',
        properties={
            'a':types.Schema(type='NUMBER'),
            'b':types.Schema(type='NUMBER')
        },
        required=['a','b']
    )
)

available_tools = types.Tool(
    function_declarations=[
        add_tool,
        sub_tool,
        mult_tool,
        div_tool,
        flrdiv_tool,
        mod_tool,
        powr_tool
    ]
)


tool_registry = {
    "add": add,
    "sub": sub,
    "mult": mult,
    "div": div,
    "flrdiv": flrdiv,
    "mod": mod,
    "powr": powr
}

instructions='''
    you are a calculator.
    claculate the numbers properly and explain it lin by line.
'''

history=[]

while True:
    question=input('Ask:')
    if question.lower() in ['exit','end','quit']:
        print('Thank u for using my calculator!')
        break

    history.append({
        'role':'user',
        'message':question
    })

    prompt=instructions+'\n\nconversasstion\n'
    for message in history:
        prompt += f"{message['role']}:{message['message']}\n" 

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[available_tools]
        )
    )
    parts = response.candidates[0].content.parts

    for part in parts:

        if part.function_call:

            tool_name = part.function_call.name
            arguments = part.function_call.args

            function = tool_registry[tool_name]

            result = function(**arguments)

            print("Tool:", tool_name)
            print("Arguments:", arguments)
            print("Result:", result)

            tool_response = types.Part.from_function_response(
                name=tool_name,
                response={
                    "result": result
                }
            )

            final_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    response.candidates[0].content,
                    types.Content(
                        role="user",
                        parts=[tool_response]
                    )
                ],
                config=types.GenerateContentConfig(
                    tools=[available_tools]
                )
            )

            print("AI:", final_response.text)