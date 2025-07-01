import os
import sys
import pikepdf
import getpass
import shutil


def is_pdf_password_protected(file_path):
    try:
        with pikepdf.open(file_path) as pdf:
            return False  # No password required
    except pikepdf.PasswordError:
        return True  # Password required
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False


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
                # Check if the PDF is password protected
                if is_pdf_password_protected(file_path):
                    # Try to open and decrypt the PDF with the provided password
                    with pikepdf.open(file_path, password=password) as pdf:
                        # Create a new filename with a "_decrypted" suffix
                        base, ext = os.path.splitext(filename)
                        new_filename = f"{base}_decrypted{ext}"
                        output_pdf_path = os.path.join(output_folder_path, new_filename)

                        # Save the decrypted PDF to the output directory
                        pdf.save(output_pdf_path)
                        print(f"Decrypted and saved: {output_pdf_path}")
                else:
                    # If not password protected, copy the file to output folder
                    base, ext = os.path.splitext(filename)
                    new_filename = f"{base}_decrypted{ext}"
                    output_pdf_path = os.path.join(output_folder_path, new_filename)
                    shutil.copy2(file_path, output_pdf_path)
                    print(f"Copied non-protected PDF: {output_pdf_path}")

            except pikepdf.PasswordError:
                print(f"Skipping {file_path}: Incorrect password")
            except Exception as e:
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
