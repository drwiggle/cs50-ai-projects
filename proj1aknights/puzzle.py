from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
puzzle0Asays = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave), # A is either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both a knight and a knave
    Biconditional(AKnight, puzzle0Asays) # A is a knight iff the the thing he said is true
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
puzzle1Asays = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnight, AKnave), # A is a knight or a knave, 
    Not(And(AKnight, AKnave)),# but not both
    Or(BKnight, BKnave), # B is a knight or a knave, 
    Not(And(BKnight, BKnave)),# but not both
    Biconditional(AKnight, puzzle1Asays) # A is a knight iff the the thing he said is true
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
puzzle2Asays = Or(And(AKnight, BKnight), And(AKnave, BKnave))
puzzle2Bsays = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Or(AKnight, AKnave), # A is a knight or a knave, 
    Not(And(AKnight, AKnave)),# but not both
    Or(BKnight, BKnave), # B is a knight or a knave, 
    Not(And(BKnight, BKnave)), # but not both
    Biconditional(AKnight, puzzle2Asays), # A is a knight iff the the thing he said is true
    Biconditional(BKnight, puzzle2Bsays) # B is a knight iff the the thing he said is true
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

puzzle3Asays = Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave))
puzzle3Bsays1 = Biconditional(AKnight, BKnave)
puzzle3Bsays2 = CKnave
puzzle3Csays = AKnight

knowledge3 = And(
    Or(AKnight, AKnave), # A is a knight or a knave, 
    Not(And(AKnight, AKnave)),# but not both
    Or(BKnight, BKnave), # B is a knight or a knave, 
    Not(And(BKnight, BKnave)),# but not both
    Or(CKnight, CKnave), # C is a knight or a knave, 
    Not(And(CKnight, CKnave)),# but not both
    Biconditional(AKnight, puzzle3Asays), # A is a knight iff the the thing he said is true
    Implication(BKnight, puzzle3Bsays1), # If B is a knight, then  the thing he said is true.  This one is not a biconditional, because if B is a knave, then we just know he's lying, in which case A could have said nothing, or could have said the opposite of what B claims.
    Biconditional(BKnight, puzzle3Bsays2), # B is a knight iff the the thing he said is true
    Biconditional(CKnight, puzzle3Csays) # B is a knight iff the the thing he said is true
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
