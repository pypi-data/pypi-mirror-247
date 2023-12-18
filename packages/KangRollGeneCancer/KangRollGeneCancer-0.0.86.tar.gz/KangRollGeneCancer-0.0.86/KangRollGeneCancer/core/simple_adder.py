# simple_adder.py

def add_numbers(a, b):
    return a + b +10

def main():
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    result = add_numbers(num1, num2)
    print("The sum is:", result)

if __name__ == "__main__":
    main()
