from langchain_experimental.llms.ollama_functions import OllamaFunctions
'''from langchain_core.messages import HumanMessage

model = OllamaFunctions(
    model="llama3.1:8b",
    format="json"
)

model = model.bind_tools(
    tools=[
        {
            "name":"get_current_weather",
            "description":"Get the current weather in a given location",
            "parameters":{
                "type":"object",
                "properties":{
                    "location":{
                        "type":"string",
                        "description":"The city and state, ""e.g. San Francisco, CA",
                    },
                    "unit":{
                        "type":"string",
                        "enum":["celsius","fahrenheit"],
                    },
                },
                "required":["location"],
            }
        }
    ],
    function_call={"name":"get_current_weather"},
)

response = model.invoke("what is the weather in Singapore?")

print(response)'''

'''from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.messages import HumanMessage

model = OllamaFunctions(
    model="llama3.1:8b",
    format="json"
)

model = model.bind_tools(
    tools=[
        {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            }
        },
        {
            "name": "subtract",
            "description": "Subtract two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            }
        },
        {
            "name": "multiply",
            "description": "Multiply two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            }
        },
        {
            "name": "divide",
            "description": "Divide two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number, should not be zero"},
                },
                "required": ["a", "b"],
            }
        }
    ],
)

response = model.invoke("What is the result of 10 divided by 2?")

print(response)
'''

from langchain_experimental.llms.ollama_functions import OllamaFunctions

model = OllamaFunctions(
    model="llama3.1:8b",
    format="json"
)

model = model.bind_tools(
    tools=[
        {
            "name": "set_alarm",
            "description": "Set an alarm or reminder at a specified time",
            "parameters": {
                "type": "object",
                "properties": {
                    "time": {"type": "string", "description": "Time for the alarm/reminder in HH:MM format (24-hour)"},
                    "date": {"type": "string", "description": "Date for the alarm/reminder in YYYY-MM-DD format"},
                    "message": {"type": "string", "description": "Message to display when the alarm goes off"},
                    "repeat": {"type": "string", "enum": ["none", "daily", "weekly", "monthly"], "description": "Set recurrence for the alarm"},
                },
                "required": ["time", "date", "message"]
            }
        },
        {
            "name": "call_person",
            "description": "Make a phone call to a specified person",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_name": {"type": "string", "description": "Full name of the person to call"},
                    "phone_number": {"type": "string", "description": "Phone number of the recipient in international format (+XX)"},
                    "reason": {"type": "string", "description": "Reason for the call (e.g., urgent, casual, work-related)"},
                },
                "required": ["contact_name", "phone_number"]
            }
        },
        {
            "name": "place_order",
            "description": "Place an order for an item or service",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {"type": "string", "description": "Name of the item/service to order"},
                    "quantity": {"type": "integer", "description": "Number of items to order"},
                    "delivery_address": {"type": "string", "description": "Address where the order should be delivered"},
                    "payment_method": {"type": "string", "enum": ["credit_card", "debit_card", "cash_on_delivery", "paypal"], "description": "Preferred payment method"},
                    "special_instructions": {"type": "string", "description": "Any additional instructions for the order", "default": ""}
                },
                "required": ["item_name", "quantity", "delivery_address", "payment_method"]
            }
        },
        {
            "name": "pay_bills",
            "description": "Pay a bill for a specific service",
            "parameters": {
                "type": "object",
                "properties": {
                    "bill_type": {"type": "string", "enum": ["electricity", "water", "internet", "phone", "rent", "credit_card"], "description": "Type of bill to pay"},
                    "amount": {"type": "number", "description": "Amount to pay"},
                    "due_date": {"type": "string", "description": "Due date of the bill in YYYY-MM-DD format"},
                    "payment_method": {"type": "string", "enum": ["credit_card", "debit_card", "bank_transfer", "paypal"], "description": "Method used for payment"},
                    "account_number": {"type": "string", "description": "Account number associated with the bill"},
                },
                "required": ["bill_type", "amount", "due_date", "payment_method", "account_number"]
            }
        }
    ],
)

'''response = model.invoke("Set an alarm for tomorrow at 7 AM with message 'Wake up for gym'.")
print(response)
response = model.invoke("Set an alarm for March 1st at 6:30 AM with message 'Go for a morning run'.")
print(response)
response = model.invoke("Call John Doe at +1234567890 for a work-related discussion.")
print(response)
response = model.invoke("Order 2 large pizzas to 123 Main Street with cash on delivery. Extra cheese, please.")
print(response)
response = model.invoke("Pay my electricity bill of $120 due on February 25th using my credit card. Account number: 987654321.")
print(response)'''


'''response = model.invoke("Call John Doe for an urgent matter.")  # Missing phone number
print(response)'''