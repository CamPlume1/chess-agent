import time
import chess
import chess.svg
import webbrowser
import os
import http.server
import socketserver
import threading

class ChessGui:
    def __init__(self, board: chess.Board):
        self.board = board
        self.server_thread = None
        self.httpd = None
        self.start_local_server()

    def start_local_server(self):
        os.makedirs('chess_boards', exist_ok=True)  # Ensure directory exists

        handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(('', 8000), handler)
        self.port_num = 8000

        def run_server():
            print("Serving at port ", self.port_num)
            self.httpd.serve_forever()
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

        # Create an HTML file that will auto-refresh the SVG
        self.create_refresh_html()

    def create_refresh_html(self):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chess Board</title>
            <meta http-equiv="refresh" content="0.25">
            <style>
                body { margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
                img { max-width: 100%; max-height: 100vh; }
            </style>
        </head>
        <body>
            <img src="current_board.svg" alt="Chess Board">
        </body>
        </html>
        """
        
        with open('chess_boards/index.html', 'w') as f:
            f.write(html_content)

    def print_board(self):
        file_path = os.path.join('chess_boards', 'current_board.svg')

        svg = chess.svg.board(self.board)
        
        # Generate SVG representation of the board and save it
        with open(file_path, 'w') as f:
            f.write(svg)
        
        # Open only once
        if not hasattr(self, 'browser_opened'):
            webbrowser.open(f'http://localhost:{self.port_num}/chess_boards/index.html')
            self.browser_opened = True

    def cleanup(self):
        if self.httpd:
            print("Shutting down server...")
            self.httpd.shutdown()
            self.httpd.server_close()




# import time
# import chess
# import chess.svg
# import webbrowser
# import os
# import http.server
# import socketserver
# import threading

# class ChessGui:
#     def __init__(self, board: chess.Board):
#         self.board = board
#         self.server_thread = None
#         self.httpd = None
#         self.start_local_server()

#     def start_local_server(self):
#         os.makedirs('chess_boards', exist_ok=True)  # Ensure directory exists

#         handler = http.server.SimpleHTTPRequestHandler
#         self.httpd = socketserver.TCPServer(('', 0), handler) 
#         self.port_num = self.httpd.server_address[1]

        
#         def run_server():
#             print("Serving at port ", self.port_num)
#             self.httpd.serve_forever()
        
#         self.server_thread = threading.Thread(target=run_server, daemon=True)
#         self.server_thread.start()

#     def print_board(self):
#         file_path = os.path.join('chess_boards', 'current_board.svg')

#         svg = chess.svg.board(self.board)
        
#         # Generate SVG representation of the board and save it
#         with open(file_path, 'w') as f:
#             f.write(svg)
        
#         url = f'http://localhost:{self.port_num}/chess_boards/current_board.svg'
#         # Open only once
#         webbrowser.open(url, new=0) # Update this to open it in the same tab

#     def cleanup(self):
#         if self.httpd:
#             print("Shutting down server...")
#             self.httpd.shutdown()
#             self.httpd.server_close()
