import random

def get_computer_choice():
    return random.choice(['stone', 'paper', 'scissor'])

def get_user_choice():
    choice = input("\nEnter your choice (stone, paper, scissor): ").lower()
    while choice not in ['stone', 'paper', 'scissor']:
        print("❌ Invalid input. Try again.")
        choice = input("Enter your choice (stone, paper, scissor): ").lower()
    return choice

def determine_winner(user, computer):
    if user == computer:
        return "🤝 It's a tie!"
    elif (user == 'stone' and computer == 'scissor') or \
         (user == 'paper' and computer == 'stone') or \
         (user == 'scissor' and computer == 'paper'):
        return "🎉 You win!"
    else:
        return "💻 Computer wins!"

def play_game():
    print("\n🎮 Welcome to the Stone-Paper-Scissor Game!")

    while True:
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()

        print(f"\n👉 You chose: {user_choice.capitalize()}")
        print(f"🤖 Computer chose: {computer_choice.capitalize()}")
        
        result = determine_winner(user_choice, computer_choice)
        print(f"🧠 Result: {result}")

        again = input("\nDo you want to play again? (yes/no): ").lower()
        if again != 'yes':
            print("👋 Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()
