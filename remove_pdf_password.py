import os
import sys
import pikepdf
import getpass


def remove_pdf_password_in_folder(input_folder_path, output_folder_path, password):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Iterate over all the files in the folder
    for filename in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, filename)
        # Check if the file is a PDF
        if file_path.lower().endswith(".pdf"):
            try:
                # Try to open the PDF with the provided password
                with pikepdf.open(file_path, password=password) as pdf:
                    # Create a new filename with a "_decrypted" suffix
                    base, ext = os.path.splitext(filename)
                    new_filename = f"{base}_decrypted{ext}"
                    output_pdf_path = os.path.join(output_folder_path, new_filename)

                    # Save the decrypted PDF to the output directory
                    pdf.save(output_pdf_path)
                    print(f"Decrypted and saved: {output_pdf_path}")

            except pikepdf.PasswordError:
                # Handle wrong password or unencrypted situation
                print(f"Skipping non-encrypted or incorrect password PDF: {file_path}")
            except Exception as e:
                # Handle any other exceptions
                print(f"An error occurred with file {file_path}: {e}")


if __name__ == "__main__":
    # Get the current directory
    current_dir = os.getcwd()

    # Convert input arguments to absolute paths
    input_folder = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else current_dir
    output_folder = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else current_dir

    # Prompt the user for the PDF password
    pdf_password = getpass.getpass(prompt="Enter PDF password: ")

    # Process the PDFs in the specified or default directories
    remove_pdf_password_in_folder(input_folder, output_folder, pdf_password)

