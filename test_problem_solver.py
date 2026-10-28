from app.problem_solver.problem_solver_manager import ProblemSolverManager


def print_result(query: str, result):
    print("=" * 80)
    print(f"Query      : {query}")
    print(f"Status     : {result.status.value}")
    print(f"Type       : {result.problem_type.value}")
    print(f"Expression : {result.expression}")
    print(f"Answer     : {result.answer}")
    print(f"Explanation: {result.explanation}")
    print(f"Error      : {result.error}")
    print("=" * 80)
    print()


def main():
    manager = ProblemSolverManager()

    test_queries = [
        # Basic Arithmetic
        "2 + 3",
        "10 - 5",
        "7 * 8",
        "100 / 4",
        "10 % 3",
        "2 ** 10",

        # Natural Language
        "What is 15 + 20?",
        "Calculate 50 divided by 5",
        "Compute 17 multiplied by 9",
        "Evaluate 25 minus 13",

        # Special Cases
        "5 squared",
        "4 cubed",
        "square root of 81",
        "half of 60",
        "quarter of 200",
        "15% of 400",

        # Decimals
        "3.5 + 2.8",
        "9.9 * 2",

        # Negative Numbers
        "-5 + 20",
        "10 + -8",

        # Error Cases
        "100 / 0",
        "5 +",
        "sqrt()",
        "abc + 5",

        # Unsupported Queries
        "Hello Jarvis",
        "How are you?",
        "Who is Iron Man?",
    ]

    for query in test_queries:
        result = manager.solve(query)
        print_result(query, result)


if __name__ == "__main__":
    main()