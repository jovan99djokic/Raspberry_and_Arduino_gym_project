import webbrowser

def open_html_file(file_path):
    # Replace backslashes in file path with forward slashes for compatibility
    file_path = file_path.replace('\\', '/')
    
    # Open the HTML file in the default web browser
    webbrowser.open('file://' + file_path)

# Example usage:
if __name__ == "__main__":
    html_file_path = '/home/raspberry/Desktop/Camera /index.html'  # Replace with your HTML file path
    open_html_file(html_file_path)
