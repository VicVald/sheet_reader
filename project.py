import cv2
import numpy as np
import os

def main():

    #Colors used in the terminal
    red = '\33[31m'
    green = '\33[32m'
    cyan = '\33[36m'

    letters_list = ['A', 'B', 'C', 'D', 'E']

    #Get the number of questions and alternatives
    questions, alternatives, right_answers = prompts()

    #Define the area of the cells in the answer sheet
    fields = answerSheetStructure(questions, alternatives)

    #Directory where the images are
    directory = 'provas'

    #Number of the test
    prova_num = 1

    for prova in os.listdir(directory):
        print('-+-'*20)

        #Open the image
        with open(os.path.join(directory, prova)) as f:
            print(f"Prova: {prova_num}")
            prova_num += 1

            #Read the image, and warp it to the right perspective and filter it
            answer_sheet, img = readImg(prova)
            imgGray = cv2.cvtColor(answer_sheet, cv2.COLOR_BGR2GRAY)
            rect, imgTh = cv2.threshold(imgGray, 70, 255, cv2.THRESH_BINARY_INV)

            #Create a list to store the user answers
            user_answers = []

            for id,vg in enumerate(fields):
                #Vg is the coordinates of each cell
                x = int(vg[0])
                y = int(vg[1])
                w = int(vg[2])
                h = int(vg[3])

                #Draw the rectangles in the image
                cv2.rectangle(answer_sheet, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.rectangle(imgTh, (x, y), (x+w, y+h), (255, 255, 255), 1)
                field = imgTh[y:y+h, x:x+w]

                #Count the black pixels in the cell
                height, width = field.shape[:2]
                size = height * width
                blacks = cv2.countNonZero(field)
                percentage = round((blacks / size) * 100, 2)

                #Condition to check as marked cell
                if percentage >= 20:
                    cv2.rectangle(answer_sheet, (x,y), (x + w, y + h), (255,8,8), 2)
                    
                    #Algorithm to identify which cell
                    answer_num = (id // alternatives) + 1
                    answer_alpha = id % alternatives
                    double_answer = False

                    i = 0
                    #Check if have two or more answers in the same row
                    for user_answer in user_answers:
                        if str(answer_num) in user_answer:
                            double_answer = True
                            user_answers[i] = f'{i+1}Z'
                        i += 1

                    if double_answer == False:
                        user_answers.append(f'{answer_num}{letters_list[answer_alpha]}')
                    
            #Check if all rows have one answer selected, if not insert a "wrong answer" to the list
            if len(user_answers) != questions:
                for i in range(questions):
                    if not any(answer.startswith(str(i+1)) for answer in user_answers):
                        user_answers.insert(i, f'{i+1}0')

            #Counters for hits and misses
            hits = 0
            misses = 0

            print()
            
            #Compare user answers with the right_answers and print the results
            for num, answer in enumerate(user_answers):
                if answer == right_answers[num]:
                    hits += 1
                    print(f"{green}Questão {num+1} correta!\n")
                elif answer.endswith('Z'):
                    print(f"{red}Questão {num+1} com duas respostas! |  A resposta é: {cyan}{right_answers[num]}\n")
                    misses += 1
                elif answer.endswith('0'):
                    print(f"{red}Questão {num+1} não respondida! |  A resposta é: {cyan}{right_answers[num]}\n")
                    misses += 1
                else:
                    print(f"{red}Questão {num+1} errada!  |  A resposta é: {cyan}{right_answers[num]}\n")
                    misses += 1

            print(f"{cyan}Acertou: {hits}\nErrou: {misses}")
            print('\033[0m' + '-+-'*20)
            print('\nAperte qualquer tecla para ver a próxima prova...\n')
            
            #Show the image
            imgs = cv2.vconcat([img, answer_sheet])
            cv2.imshow('Prova', imgs)
            if (cv2.waitKey(0) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
            
def askUntilValid(question, error_message, condition):

    #Loop to ask the question until the user gives a valid answer
    while True:
        response = input(question)
        if condition(response):
            return response
        else:
            print(error_message)


def prompts():

    #Ask for the number of questions and alternatives
    questions = int(askUntilValid(
        "Quantas questões tem a prova? ",
        "Digite um número válido de questões! (1-15)",
        lambda x: 0 < int(x) <= 15
    ))
    alternatives = askUntilValid(
        "Até qual letra vão as questões? ",
        "Digite um valor válido de letras! (D ou E)",
        lambda x: x.upper() in ['D', 'E']
    ).upper()

    #Get the right answers to compare with the user answers
    right_answers = []
    for i in range(questions):
        answer = askUntilValid(
            f"Digite a resposta da questão {i+1}: ",
            "Digite uma resposta válida! (A, B, C, D ou E)",
            lambda x: x.upper() in ['A', 'B', 'C', 'D', 'E']
        )
        right_answers.append(f'{i+1}{answer.upper()}')

    match alternatives.upper():
        case 'D':
            alternatives = 4
        case 'E':
            alternatives = 5

    return questions, alternatives, right_answers


def answerSheetStructure(questions, letters):

    #Create the structure of the ROI's to each question
    fields = []
    #Loop for rows
    for i in range(questions):
        #Loop for columns
        for j in range(letters):
            if i==14:
                fields.append((48 + j*48,4+i*26.5,48,20))
            else:
                fields.append((48 + j*48,4+i*26.5,48,25))
            
    return fields


def readImg(path):

    #Filtering the image
    img = cv2.imread(f"/home/victorhugo/Code/project/provas/{path}")
    if img is None:
        raise ValueError(f"Could not read image at path: {path}")
    
    realimg=img
    realimg = cv2.resize(realimg, (290, 399))
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    countours, hi = cv2.findContours(imgTh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    greaterCtn = max(countours, key=cv2.contourArea)
    
    x, y, w, h = cv2.boundingRect(greaterCtn)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #Crop the image approximately
    answer_sheet = img[y:y+h, x:x+w]
    answer_sheet = cv2.resize(answer_sheet, (290, 399))

    #Warp to the right perspective
    warped_answer_sheet = warpImg(answer_sheet)
    

    return warped_answer_sheet, realimg


def warpImg(img):

    #Filter the cropped image and get edges and the biggest contour
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    edges = cv2.Canny(gray, 30, 200)
    countours, hi = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    countours = sorted(countours, key=cv2.contourArea, reverse=True)[:1]

    #Create the perspective transformation and draw the rectangle
    for i in countours:
        cv2.drawContours(img, [i], -1, (0, 255, 0), 3)
        points = cv2.approxPolyDP(i, 0.02*cv2.arcLength(i, True), True)
        if len(points) == 4:
            points = points.reshape((4, 2))
            original_points = np.float32([points[0], points[1], points[3], points[2]])
            new_points = np.float32([[0, 0], [0, 399], [290, 0], [290, 399]])
            perspective = cv2.getPerspectiveTransform(original_points, new_points)
            result = cv2.warpPerspective(img, perspective, (290, 399))            
        else:
            raise ValueError("Could not find the contour of the image")

    return result



if __name__ == '__main__':
    main()
