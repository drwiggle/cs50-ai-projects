from nim import train, play

ai = train(10000)
while True:
    play(ai)
    play_again = input("Do you want to play again? (Y/N): ")
    if play_again.lower() not in {"y", "yes"}:
        break
