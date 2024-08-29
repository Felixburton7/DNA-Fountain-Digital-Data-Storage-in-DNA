# CSE 487 Advanced Systems and Synthetic Biology

### Summary for the DNA Fountain Project - DNA Digital Data Storage

This repo contains a Python script for a project centered around DNA Fountain technology, which demonstrates the encoding and processing of digital data into DNA sequences for potential digital storage applications. The script performs the following tasks:

1. **Data Encoding:**
   - Encodes digital data into DNA sequences using a predefined encoding scheme.

2. **Luby Transform Code:**
   - Utilizes Luby Transform (LT) codes to encode the data into DNA droplets, providing robustness and error correction capabilities.

3. **DNA Sequence Processing:**
   - Processes the DNA droplets, handling different block indices and generating binary sequences.

4. **Error Handling:**
   - Includes error handling to manage unexpected bases and out-of-range indices during the droplet processing.

5. **Output Generation:**
   - Outputs the encoded DNA sequences and provides a final decoded message.

The script is designed to explore the potential of DNA as a medium for digital data storage, showcasing the feasibility and challenges of encoding and decoding digital information using biological molecules.
#
### Usage

To run the script:
1. Ensure you have Python installed.
2. Navigate to the project directory.
3. Execute the script using Python:
   ```sh
   python DNA_Fountain_Project_1.py
   ```

### Requirements

- Python 3.x
- Pygments (for syntax highlighting, if converting to HTML)
- Pandoc (for converting HTML to PDF, optional)
- MiKTeX (for `pdflatex`, optional)

### File Structure

- `DNA_Fountain_Project_1.py`: Main script file containing the DNA Fountain encoding and processing logic.
- `DNA_Fountain_Project_1.html`: HTML file generated from the script (optional, for conversion to PDF).
- `luby_blocks.csv`: CSV file containing Luby Transform blocks data.

### Conversion to PDF

For convenience, the script can be converted to a PDF file using Pandoc and `pdflatex`. Follow these steps:

1. Convert Python script to HTML:
   ```sh
   pygmentize -f html -O full,style=colorful -o DNA_Fountain_Project_1.html DNA_Fountain_Project_1.py
   ```
2. Convert HTML to PDF:
   ```sh
   pandoc DNA_Fountain_Project_1.html -o DNA_Fountain_Project_1.pdf
   ```
### Picture representation of project
![image](https://github.com/Felixburton7/CSE-487-Advanced-Systems-and-Synthetic-Biology-/assets/106174577/31b1c46d-e30e-4eee-8700-47b9d9617971)


### License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to contribute to this project by opening issues and submitting pull requests, or send me a message at felixburton2002@gmail.com

