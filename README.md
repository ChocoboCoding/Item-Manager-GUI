# 🔧 Item Manager GUI

A simple, user-friendly Python GUI application built with `tkinter` that lets you manage, search, and output item data for game development or inventory systems.

## 📦 Features

- Add and update items with:
  - Item Name
  - Item ID
  - Item String
- Dynamic search through items by name, ID, or string
- Double-click to autofill fields from item list
- JSON input parser for item data
- Output item as a formatted JSON string with customizable amount
- Undo/Redo support
- Persistent data saved in `items_data.txt`
- Clipboard auto-copy for generated JSON

## ⚙️ Requirements

- Python 3.x
- No external libraries needed – uses standard `tkinter` and `json`

## 🚀 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/item-manager-gui.git
cd item-manager-gui
```

2. Run the app:

```bash
python item_manager.py
```

## 📝 Notes

- Ensure that the items_data.txt file is in the same directory as the script. It will be created automatically if missing.

- You must select an item from the list before outputting a JSON string.

- The amount field must be a number greater than zero.

## 📄 License

MIT License
