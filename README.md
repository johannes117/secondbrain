# Simple Offline MyMind Clone

This project is a simplified offline version of the MyMind application built with Streamlit. It allows users to create, view, and search for "cards" stored in a JSON format in a local SQLite database.

## Features

- Add new cards with content
- View all saved cards
- Fuzzy search through cards based on their content

## Requirements

- Python 3.7 or higher
- Streamlit
- Pandas
- Fuzzywuzzy
- Python-Levenshtein

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/mymind-clone.git
    cd mymind-clone
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment:**
    - On macOS and Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

4. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Activate the virtual environment (if not already activated):**
    - On macOS and Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

2. **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

## Usage

### Add a New Card

1. Select "Add Card" from the sidebar.
2. Enter the content of the card in the provided text area.
3. Click the "Add Card" button to save the card.

### View All Cards

1. Select "View All Cards" from the sidebar.
2. All saved cards will be displayed.

### Search Cards

1. Select "Search Cards" from the sidebar.
2. Enter a search query in the input box.
3. Adjust the fuzzy match threshold using the slider.
4. Click the "Search" button to find matching cards.

## Dependencies

- streamlit==1.19.0
- pandas==1.4.2
- fuzzywuzzy==0.18.0
- python-Levenshtein==0.12.2

These dependencies are listed in the `requirements.txt` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
- [Python-Levenshtein](https://github.com/ztane/python-Levenshtein)

