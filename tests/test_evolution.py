from app.evolution import load_evolution_memory


def main():
    memory = load_evolution_memory()

    print("Evolution memory loaded successfully.")
    print(memory)


if __name__ == "__main__":
    main()