import random, csv

class magic8ball:

    # add the init function
    def __init__(self):
        self.__mQuestions = []
        self.__response_list = [
            'Yes, absolutely',
            'Not a chance',
            'Get a life',
            'No doubt',
            'Si Dios quiere',
            'Only if you really want it',
            'How much are you willing to pay me for it?',
            'That would be awesome, wouldnt it?',
            'Yes, that will happen tomorrow',
            'You were destined for it'
        ]
        self.__welcome()
        self.__start_game()
        
    
    # create a private method for the game
    def __start_game(self):
        question = 'Starter'
        while question != '':
            question = input('Please enter your question: ')
            if question != '':
                self.__mQuestions.append(question)
                n = random.randint(0,9)
                print(self.__response_list[n])
            else:
                print('Thank you for playing!')
                # self.__write_questions()
            
    # create private method to welcome user
    def __welcome(self):
        name = input('Enter your name to begin the game: ')
        print(f'Welcome, {name}!! Thanks for playing. Press enter without entering a question when you are done playing.')
        
    # # create a private method to write to a csv file
    # def __write_questions(self):
    #     f = open('magic_questions.csv', 'a')
    #     wrt = csv.writer(f)
    #     for q in self.__mQuestions:
    #         wrt.writerow([q])
    #     f.close()

# # this code is used if you are going to play from the console
# name = input("Please enter your name to begin playing: ")
# new_game = magic8ball(name)