import os
import tkinter as tk
from tkinter import scrolledtext
import asyncio
from openai import OpenAI

root = tk.Tk()
root.title("Intimisfera")
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)

def disable_event():
    return

root.protocol("WM_DELETE_WINDOW", disable_event)
root.bind("<Alt-F4>", disable_event)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

bg_color = "#2d2d2d"
fg_color = "#ffffff"
entry_bg = "#3d3d3d"
button_bg = "#4d4d4d"
font_size = 25
root.configure(bg=bg_color)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Courier", font_size), bg=bg_color, fg=fg_color, insertbackground=fg_color)
output_text.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=int(screen_width * 0.05), pady=int(screen_height * 0.01))

input_frame = tk.Frame(root, bg=bg_color)
input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=int(screen_width * 0.005), pady=int(screen_height * 0.002))

input_label = tk.Label(input_frame, text="Input:", font=("Courier", font_size), bg=bg_color, fg=fg_color)
input_label.pack(side=tk.LEFT, padx=int(screen_width * 0.01))

input_entry = tk.Entry(input_frame, width=int(screen_width * 0.02), font=("Courier", font_size), bg=entry_bg, fg=fg_color, insertbackground=fg_color)
input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=int(screen_width * 0.005))

submit_button = tk.Button(input_frame, text="Submit", font=("Courier", font_size), bg=button_bg, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
submit_button.pack(side=tk.LEFT, padx=int(screen_width * 0.005))

user_input = ""

def clear_all():
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)

def display_message(message, msg_type=None):
    if msg_type:
        message = str(message).replace("*", "")
        message = message.replace("#", "")
        output_text.config(font=("Courier", font_size-6))
    else:
        output_text.config(font=("Courier", font_size - 6))

    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, str(message) + "\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)

game_task = None
def reset_game():
    global game_task
    if game_task is not None:
        game_task.cancel()
    clear_all()
    game_task = loop.create_task(play_game())

async def get_input(prompt):
    global future
    display_message(prompt)
    input_entry.delete(0, tk.END)
    input_entry.focus()

    future = asyncio.Future()

    def on_submit(event=None):
        if not future.done():
            user_input = input_entry.get()
            if ("reset" in user_input.lower()) or ("restart" in user_input.lower()):
                reset_game()
                return

            elif user_input == "":
                return

            elif (user_input.lower() == "close") or (user_input.lower() == "kill") or (user_input.lower() == "shut down"):
                os.system("taskkill /IM python.exe /F")
                os.system("taskkill /IM intimisfera.exe /F")
                return

            future.set_result(user_input)
            display_message(f"> {user_input}\n")
            input_entry.delete(0, tk.END)
            input_entry.focus()

    submit_button.config(command=on_submit)
    input_entry.bind("<Return>", on_submit)

    return await future

openai_api_key = "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"

def deepseek_response(all_responses):
    interpretare_prompt = f"""
        {all_responses}

        Mai sus ai un dictionar cu toate intrebarile si raspunsurile date la un chestionar despre intimitate, trebuie sa interpretezi firecare raspuns, fara o concluzie, detaliata dupa exemplul de mai jos, fara sa folosi text de introducere, cum ar fi "desigur, iata...", arata direct interpretarea, te rog: 

        Ceilalti te vad ca un/o {all_responses['animal_domestic']['Raspuns']}, pentru ca esti {all_responses['de_ce_animal_domestic']['Raspuns']}
        Tu te vezi ca un/o {all_responses['animal_salbatic']['Raspuns']}, pentru ca esti {all_responses['de_ce_animal_salbatic']['Raspuns']}
        Tu vezi relatia de cuplu cu {all_responses['sentiment']['Raspuns']}
        Activitatea sexuala pentru tine este: {all_responses['3 caracteristici a felului de mancare preferat']}

        Exemplul nu trebuie sa fie folosit asa cum este el, trebuie extins cu detali si alte lucruiri.
        Daca nu poti interpreta raspunsurile date sau daca nu sunt raspunsuri bune din partea user-ului, spune ca interpretarea a esuat.
        """

    client = OpenAI(api_key="sk-b93698819fd948958ca38360a485d93b", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": interpretare_prompt},
            {"role": "user", "content": "Te rog sa imi interpretezi raspunsurile."},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content

async def play_game():
    clear_all()

    display_message("\nHey TU! Eu sunt Intimisfera si pot sa-ti spun cate ceva despre tine. Try me!\n")

    # ----------- INTEROGARE ------------------------------------------------------------------------------------
    animal_domestic_iti_place = await get_input("Ce animal domestic iti place?")
    animal_domestic_iti_place_dece = await get_input("pentru ca este...")

    daca_ai_fi_animal_salbatic = await get_input("Daca ai fi un animal salbatic ai fi...")
    daca_ai_fi_animal_salbatic_ptr_ca = await get_input("pentru ca este...")

    sentiment = await get_input("Daca ai fi intr-o camera alba fara geamuri si usi, ce sentiment ai simti?")

    fel_macare_caract_1 = await get_input("Zi-mi 3 caracteristici a felului de mancare preferat:\n1. ")
    fel_macare_caract_2 = await get_input("2. ")
    fel_macare_caract_3 = await get_input("3. ")

    display_message("Se realizeaza interpretarea...")

    await asyncio.sleep(0.5)

    # ----------- INTERPRETARE ------------------------------------------------------------------------------------
    all_responses = {
        "animal_domestic": {"Intrebare": "Ce animal domestic iti place?", "Raspuns": animal_domestic_iti_place},
        "de_ce_animal_domestic": {"Intrebare": "pentru ca este...", "Raspuns": animal_domestic_iti_place_dece},
        "animal_salbatic": {"Intrebare": "Ce animal domestic iti place?", "Raspuns": daca_ai_fi_animal_salbatic},
        "de_ce_animal_salbatic": {"Intrebare": "pentru ca este...", "Raspuns": daca_ai_fi_animal_salbatic_ptr_ca},
        "sentiment": {"Intrebare": "Daca ai fi intr-o camera alba fara geamuri si usi, ce sentiment ai trai?", "Raspuns": sentiment},
        "3 caracteristici a felului de mancare preferat": [fel_macare_caract_1, fel_macare_caract_2, fel_macare_caract_3]
    }

    interpretare_raspuns = deepseek_response(all_responses)
    clear_all()

    display_message("Conform algoritmului meu:\n\n")

    await asyncio.sleep(0.5)
    display_message(interpretare_raspuns, "d")

    """display_message(f"Ceilalti te vad ca un/o {animal_domestic_iti_place.lower()}, pentru ca esti {animal_domestic_iti_place_dece.lower()}\n")
    display_message(f"Tu te vezi ca un/o {daca_ai_fi_animal_salbatic.lower()}, pentru ca esti {daca_ai_fi_animal_salbatic_ptr_ca.lower()}\n")
    display_message(f'Tu vezi relatia de cuplu cu {sentiment.lower()}\n')
    display_message(f'Activitatea sexuala pentru tine este: {fel_macare_caract_1.lower()}, {fel_macare_caract_2.lower()}, {fel_macare_caract_3.lower()}\n')"""

reset_button = tk.Button(root, text="R", font=("Courier", font_size), bg=button_bg, fg=fg_color, activebackground=bg_color, activeforeground=fg_color, command=reset_game)
reset_button.grid(row=0, column=1, sticky="ne", padx=int(screen_width * 0.01), pady=int(screen_height * 0.02))
root.bind("<Up>", lambda event: reset_game())

async def auto_focus():
    while True:
        input_entry.focus()
        await asyncio.sleep(3)

async def run_async_tasks():
    await play_game()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(run_async_tasks())
loop.create_task(auto_focus())

def poll_asyncio():
    loop.stop()
    loop.run_forever()
    root.after(100, poll_asyncio)

poll_asyncio()
root.mainloop()
