import tkinter as tk
from tkinter import ttk
import json
import os
import copy

history_stack = []
redo_stack = []
MAX_HISTORY = 10

def get_current_state():
    return {
        "entry_item_name": entry_item_name.get(),
        "entry_item_id": entry_item_id.get(),
        "entry_item_string": entry_item_string.get(),
        "entry_json": entry_json.get()
    }

def restore_state(state):
    entry_item_name.delete(0, tk.END)
    entry_item_name.insert(0, state["entry_item_name"])
    entry_item_id.delete(0, tk.END)
    entry_item_id.insert(0, state["entry_item_id"])
    entry_item_string.delete(0, tk.END)
    entry_item_string.insert(0, state["entry_item_string"])
    entry_json.delete(0, tk.END)
    entry_json.insert(0, state["entry_json"])

def record_state():
    current = get_current_state()
    history_stack.append(copy.deepcopy(current))
    if len(history_stack) > MAX_HISTORY:
        history_stack.pop(0)
    redo_stack.clear()

def undo(event=None):
    if history_stack:
        state = history_stack.pop()
        redo_stack.append(get_current_state())
        restore_state(state)
        update_item_list(search_var.get())  # ← refresh filtered item list

def redo(event=None):
    if redo_stack:
        state = redo_stack.pop()
        history_stack.append(get_current_state())
        restore_state(state)
        update_item_list(search_var.get())  # ← refresh filtered item list

def load_from_file():
    file_path = os.path.join(os.getcwd(), "items_data.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_to_file(data):
    file_path = os.path.join(os.getcwd(), "items_data.txt")
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def add_item():
    record_state()

    item_name = entry_item_name.get().strip()
    item_id = entry_item_id.get().strip()
    item_string = entry_item_string.get().strip()

    # Check if any field is empty
    if not item_name or not item_id or not item_string:
        label_message.config(text="All fields are required.", fg="red")
        return

    item = {
        "item_name": item_name,
        "item_id": item_id,
        "item_string": item_string
    }

    # Check if item exists and override it
    for i, existing_item in enumerate(items_list):
        if existing_item["item_name"] == item_name and existing_item["item_id"] == item_id:
            items_list[i] = item
            break
    else:
        items_list.append(item)

    save_to_file(items_list)

    entry_item_name.delete(0, tk.END)
    entry_item_id.delete(0, tk.END)
    entry_item_string.delete(0, tk.END)

    update_item_list(search_var.get())
    label_message.config(text="Item saved successfully!", fg="green")

def update_item_list(filter_text=""):
    for row in treeview.get_children():
        treeview.delete(row)

    filtered_items = [
        item for item in items_list
        if filter_text.lower() in item["item_name"].lower()
           or filter_text.lower() in item["item_id"].lower()
           or filter_text.lower() in item["item_string"].lower()
    ]

    sorted_items = sorted(filtered_items, key=lambda x: x['item_name'].lower())
    for item in sorted_items:
        treeview.insert('', 'end', values=(item["item_name"], item["item_id"], item["item_string"]))

def on_item_double_click(event):
    selected_item = treeview.selection()
    if selected_item:
        item_values = treeview.item(selected_item)["values"]
        entry_item_name.delete(0, tk.END)
        entry_item_name.insert(0, item_values[0])
        entry_item_id.delete(0, tk.END)
        entry_item_id.insert(0, item_values[1])
        entry_item_string.delete(0, tk.END)
        entry_item_string.insert(0, item_values[2])

def parse_json():
    record_state()
    try:
        json_string = entry_json.get()
        parsed_data = json.loads(json_string)
        item_id = parsed_data.get("itemId", "")
        base_item_id = parsed_data.get("baseItemId", "")
        entry_item_id.delete(0, tk.END)
        entry_item_id.insert(0, item_id)
        entry_item_string.delete(0, tk.END)
        entry_item_string.insert(0, base_item_id)
        entry_json.delete(0, tk.END)  # ← This line clears the JSON input field
        label_message.config(text="Parsed successfully!", fg="green")
    except json.JSONDecodeError:
        label_message.config(text="Invalid JSON format!", fg="red")


def on_search_entry_change(*args):
    search_term = search_var.get()
    update_item_list(search_term)

def delete_selected_item(event=None):
    selected = treeview.selection()
    if not selected:
        return

    for item in selected:
        values = treeview.item(item)["values"]
        item_name, item_id = values[0], values[1]
        items_list[:] = [i for i in items_list if not (i["item_name"] == item_name and i["item_id"] == item_id)]

    save_to_file(items_list)
    update_item_list(search_var.get())
    label_message.config(text="Item deleted.", fg="blue")


root = tk.Tk()
root.title("Item Input Form")

items_list = load_from_file()

# JSON input field (top)
frame_json = tk.Frame(root)
frame_json.pack(pady=5)

tk.Label(frame_json, text="JSON Input:").grid(row=0, column=0, sticky="w", padx=5)
entry_json = tk.Entry(frame_json, width=100)
entry_json.grid(row=0, column=1, padx=5)
button_parse_json = tk.Button(frame_json, text="Parse JSON", command=parse_json)
button_parse_json.grid(row=0, column=2, padx=5, sticky="n")

# Entry fields and 'Add' button
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=5)

entry_item_name = tk.Entry(frame_inputs, width=25)
entry_item_name.grid(row=0, column=0, padx=5)
entry_item_id = tk.Entry(frame_inputs, width=25)
entry_item_id.grid(row=0, column=1, padx=5)
entry_item_string = tk.Entry(frame_inputs, width=25)
entry_item_string.grid(row=0, column=2, padx=5)

button_add_item = tk.Button(frame_inputs, text="Add Item", command=add_item)
button_add_item.grid(row=0, column=3, padx=5, sticky="n")

# Confirmation label
label_message = tk.Label(root, text="", fg="red")
label_message.pack()

# Search bar (dynamic update)
frame_search = tk.Frame(root)
frame_search.pack(pady=10)

tk.Label(frame_search, text="Search Item Name:").pack(side="left", padx=5)
search_var = tk.StringVar()
entry_search = tk.Entry(frame_search, textvariable=search_var, width=50)
entry_search.pack(side="left", padx=5)
search_var.trace("w", on_search_entry_change)  # Trace changes to update dynamically

# Amount + Output
frame_output = tk.Frame(root)
frame_output.pack(pady=5)

tk.Label(frame_output, text="Amount:").grid(row=0, column=0, padx=5)
entry_amount = tk.Entry(frame_output, width=10)
entry_amount.grid(row=0, column=1, padx=5)
entry_amount.insert(0, "1")  # ← Default value

def output_item_json():
    item_id = entry_item_id.get().strip()
    base_item_id = entry_item_string.get().strip()

    # Check if item is selected
    if not item_id or not base_item_id:
        label_message.config(text="Please select an item from the list below first.", fg="red")
        return

    # Validate amount
    try:
        amount = int(entry_amount.get())
        if amount < 1:
            raise ValueError
    except ValueError:
        label_message.config(text="Amount must be a number greater than 0", fg="red")
        return

    item_data = {
        "itemId": item_id,
        "baseItemId": base_item_id,
        "primaryVanityId": 0,
        "secondaryVanityId": 0,
        "amount": amount,
        "durability": -1,
        "modData": {"m": []},
        "rolledPerks": [],
        "insurance": "",
        "insuranceOwnerPlayfabId": "",
        "insuredAttachmentId": "",
        "origin": {"t": "", "p": "", "g": ""}
    }

    json_output = json.dumps(item_data)

    entry_output_string.config(state='normal')
    entry_output_string.delete(0, tk.END)
    entry_output_string.insert(0, json_output)
    entry_output_string.config(state='readonly')

    root.clipboard_clear()
    root.clipboard_append(json_output)
    root.update()

    entry_amount.delete(0, tk.END)
    entry_amount.insert(0, "1")
    label_message.config(text="Item JSON copied to clipboard!", fg="green")


button_output_item = tk.Button(frame_output, text="Output Item", command=output_item_json)
button_output_item.grid(row=0, column=2, padx=5)

entry_output_string = tk.Entry(frame_output, width=100, state='readonly')
entry_output_string.grid(row=0, column=3, padx=5)


# Treeview list
columns = ("Item Name", "Item ID", "Item String")
treeview = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    treeview.heading(col, text=col)
treeview.pack(pady=10)
treeview.bind("<Double-1>", on_item_double_click)

# Initial population of list
update_item_list()

root.bind('<Control-z>', undo)
root.bind('<Control-y>', redo)
root.bind('<Delete>', delete_selected_item)

root.mainloop()
