import ollama

MODEL_NAME = "qwen3.5:4b"

def generate_response(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    prompt = input("Pose ta question : ")

    response = generate_response(prompt)

    print("\nRéponse de Qwen :")
    print(response)