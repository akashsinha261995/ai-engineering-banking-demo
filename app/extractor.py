# import json

# from llm import ask_llm
# from models import CustomerPayment


# def extract_customer_data(text: str) -> CustomerPayment:

#     schema = {
#         "type": "json_schema",
#         "json_schema": {
#             "name": "customer_payment",
#             "strict": True,
#             "schema": {
#                 "type": "object",
#                 "properties": {
#                     "customer": {
#                         "type": "string"
#                     },
#                     "amount": {
#                         "type": "number"
#                     },
#                     "currency": {
#                         "type": "string"
#                     },
#                     "payment_date": {
#                         "type": ["string", "null"]
#                     }
#                 },
#                 "required": [
#                     "customer",
#                     "amount",
#                     "currency",
#                     "payment_date"
#                 ],
#                 "additionalProperties": False
#             }
#         }
#     }

#     response = ask_llm(
#         [
#             {
#                 "role": "system",
#                 "content": (
#                     "Extract customer payment information. "
#                     "Return the requested structured data."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": text
#             }
#         ],
#         response_format=schema,
#     )

#     print("\nRAW LLM RESPONSE:")
#     print(repr(response))
#     data = json.loads(response)

#     return CustomerPayment.model_validate(data)
