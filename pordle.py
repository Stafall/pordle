import tkinter as tk
import random

root = tk.Tk()
root.title("Pordle")
root.geometry("1920x1080")

body = tk.Frame(root, pady=100, bg="white")
body.pack(fill=tk.BOTH, expand=True)

words = ["tree", "moon", "blue", "calm", "rock", "fish", "star", "wind", "fire", "snow"]


grid = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
]

wod = random.choice(words).upper()
visitedRows = []

gs = {
    "cursor": 0,
    "innerCursor": 0,
    "answer": "",
    "running": True
}

def colorCompute(ans):
    color = {}
    for i in range(4):
        k = str(i)+ans[i]
        upAns = ans[i]
        if upAns == wod[i]:
            color[k] = "#98ff8f"
        elif ans[i] not in wod:
            color[k] = "#f2f2f2"
        else:
            color[k] = "#fffd8f"
    return color

def colorBlock(row, column, blocksContainer):
    txt = '' if grid[row][column] == 0 else grid[row][column]
    if type(grid[row][column]) == str and 0 not in grid[row] and row in visitedRows:
        rowWord = "".join(grid[row])
        coloredPosition = colorCompute(rowWord)
        bg = coloredPosition[str(column)+grid[row][column]]
        btn = tk.Button(
            blocksContainer, 
            relief="groove", 
            bg=bg, bd=2, height=2, width=5, 
            text=txt, font=("Helvetica", 24, "bold")
        )
        btn.grid(row=0, column=column, sticky="ew", padx=10, pady=5)
    else:
        txt = '' if grid[row][column] == 0 else grid[row][column]
        bg = '#f2f2f2' if row in visitedRows else 'white'
        btn = tk.Button(
            blocksContainer, 
            relief="groove", 
            bg=bg, bd=2, height=2, width=5, 
            text=txt, font=("Helvetica", 24, "bold")
        )
        btn.grid(row=0, column=column, sticky="ew", padx=10, pady=5)


def gridRender(con="no"):
    for widget in body.winfo_children():
        widget.destroy() 
    for row in range(4):
        blocksContainer = tk.Frame(body, bg="white", pady=10, padx=10)
        blocksContainer.pack()
        for column in range(4):
            colorBlock(row, column, blocksContainer)

gridRender()



def keyPress(event):
    #print(event.keysym)
    if not gs["running"]:
        return

    if event.keysym == "BackSpace" and gs["innerCursor"] > 0:
        gs["innerCursor"] -= 1
        gs["answer"] = gs["answer"][0:gs["innerCursor"]]
        grid[gs["cursor"]][gs["innerCursor"]] = 0
        gridRender()
        return
    
    if event.keysym == "Return" and len(gs["answer"]) == 4:
        visitedRows.append(gs["cursor"])
        gridRender("checkAnswer")
        if gs["answer"] == wod:
            gs["running"] = False
            return
        if gs["cursor"] == 3:
            gs["running"] = False
            return print("Game Over!")
        gs["answer"] = ""
        gs["innerCursor"] = 0
        gs["cursor"] += 1

    if len(gs["answer"]) < 4 and event.char.isalpha():
        letter = event.char
        gs["answer"] += letter.upper()
        grid[gs["cursor"]][gs["innerCursor"]] = letter.upper()
        gs["innerCursor"] += 1
        gridRender()



root.bind("<KeyPress>", keyPress)

def reset():
    global grid, gs, visitedRows, wod
    grid = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],  
        [0,0,0,0]
    ]
    visitedRows = []
    gs = {
        "cursor": 0,
        "innerCursor": 0,
        "answer": "",
        "running": True
    }
    wod = random.choice(words).upper()
    gridRender()

lowerhalf = tk.Frame(root, bg="#242424", pady=10)
lowerhalf.pack(fill=tk.BOTH, expand=True)

btn = tk.Button(lowerhalf, relief="flat", bg="white", height=2, width=8, text="RESET", font=("Helvetica", 12), command=reset)
btn.pack(padx=100)

root.mainloop()

