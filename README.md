# Quick Papers

**Quick Papers** is a lightweight, fast, and minimal application designed to streamline the process of downloading **Cambridge Past Papers** for CAIE examinations.  

Whether you're preparing for **AS & A Level** or **O Level** exams, Quick Papers allows you to retrieve question papers and marking schemes effortlessly using subject codes.

## Features

- **Fast & Efficient**: Download past papers directly in seconds.
- **Support for CAIE Exams**:
  - **AS & A Level**
  - **O Level**
  - **Pre U**
- **Minimal UI**: Easy-to-use, distraction-free interface.
- **Customizable Parameters**:
  - Session (June/November)
  - Year (2010–2024)
  - Paper Type (Question Paper or Marking Scheme)
  - Paper & Variant Numbers


## How It Works

1. Enter the **subject code** (e.g., `9709` for Mathematics).
2. Select:
   - **Session**: June (`s`) or November (`w`)
   - **Year**: From 2010 to 2024
   - **Paper Type**: `qp` (Question Paper) or `ms` (Marking Scheme)
   - **Paper**: 1, 2, 3, or 4
   - **Variant**: 1, 2, or 3
3. Click **Download** — and the app fetches the paper for you!


## Installation

### Prerequisites
- **Python 3.x**
- **PySide6** (for GUI)
- **Requests** (for downloading PDFs)

### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/therealhussainali/quickpapers.git
   cd quickpapers
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```


## Usage

1. Launch the app.
2. Input your desired parameters:
   - Subject Code (e.g., `9709` for Mathematics)
   - Session
   - Year
   - Paper Type
   - Paper and Variant numbers
3. Download your paper — it’s that easy!


## Screenshot

![Imgur Image][https://imgur.com/a/fjjUTVU.png]


## Contributing

Feel free to fork this project, open issues, or submit pull requests. All contributions are welcome!


## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.


## Acknowledgments

- Inspired by the need for a **faster, simpler way** to access Cambridge Past Papers.
- Built with Python and PySide6.

