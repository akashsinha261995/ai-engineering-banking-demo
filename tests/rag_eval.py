from app.chroma_store import search_chroma
from app.llm import ask_llm


test_cases = [
    {
        "question": "How long do I have to request a refund?",
        "expected_source": "Customer Refund Policy",
        "expected_keywords": ["7 days"],
    },
    {
        "question": "How long does a refund take to process?",
        "expected_source": "Customer Refund Policy",
        "expected_keywords": ["5 business days"],
    },
    {
        "question": "What are the customer support hours?",
        "expected_source": "Customer Support",
        "expected_keywords": ["9 AM", "6 PM", "Saturday"],
    },
    {
        "question": "When should an urgent payment issue be escalated?",
        "expected_source": "Customer Support",
        "expected_keywords": ["support manager"],
    },
    {
        "question": "Can a payment exceed the outstanding balance?",
        "expected_source": "Payment Policy",
        "expected_keywords": ["cannot exceed"],
    },
    {
        "question": "What is the employee maternity leave policy?",
        "expected_source": None,
        "expected_keywords": None,
    },
    {
        "question": "Can I get my money back after buying something?",
        "expected_source": "Customer Refund Policy",
        "expected_keywords": ["7 days"],
    },
]


passed = 0

for test in test_cases:

    results = search_chroma(
        test["question"],
        top_k=1,
        max_distance=1.0
    )

    documents = results["documents"][0]

    print("Retrieved:", documents)
    print("Distances:", results["distances"][0])
    print(f"{test['question']} ->")

    # No relevant knowledge found
    if test["expected_source"] is None:

        if len(documents) == 0:
            print(f"PASS: {test['question']}")
            passed += 1
        else:
            print(f"FAIL: {test['question']}")

        continue

    # Check retrieval
    if (
        len(documents) == 0
        or test["expected_source"] not in documents[0]
    ):
        print(f"FAIL: {test['question']} - wrong retrieval")
        continue

    # Build context
    context = "\n\n".join(documents)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a customer support assistant. "
                "Answer the user's question using only the "
                "provided context. "
                "If the context does not contain the answer, "
                "say that you don't know."
            )
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Question:\n{test['question']}"
            )
        }
    ]

    # Ask LLM
    response = ask_llm(messages)

    answer = response.choices[0].message.content

    # Normalize answer
    normalized_answer = (
        answer
        .lower()
        .replace("\u202f", " ")
        .replace("\xa0", " ")
    )

    # Evaluate answer using expected keywords
    expected_keywords = test["expected_keywords"]

    all_keywords_found = all(
        keyword.lower() in normalized_answer
        for keyword in expected_keywords
    )

    if all_keywords_found:
        print(f"PASS: {test['question']}")
        passed += 1
    else:
        print(f"FAIL: {test['question']}")
        print(f"Expected keywords: {expected_keywords}")
        print(f"Actual: {answer}")


print()
print(f"Passed: {passed}/{len(test_cases)}")