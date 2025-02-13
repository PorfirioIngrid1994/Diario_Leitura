import flet as ft
import json
import os

# Caminho do arquivo JSON
JSON_FILE = "books.json"

# Função para carregar os dados do JSON
def load_books():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Função para salvar os dados no JSON
def save_books(books):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

# Função para alternar o tema da aplicação
def toggle_theme(page: ft.Page, switch: ft.Switch):
    page.theme_mode = ft.ThemeMode.LIGHT if switch.value else ft.ThemeMode.DARK
    page.update()

def main(page: ft.Page):
    page.title = "Diário de Leituras"
    page.theme_mode = ft.ThemeMode.DARK # Inicia no modo escuro
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    books = load_books()

    # Botão de alternância de tema
    theme_switch = ft.Switch(value=False, on_change=lambda e: toggle_theme(page, theme_switch))

    # Imagem decorativa
    image = ft.Image(src=r"C:\\Users\\Ingrid\\OneDrive\\Documentos\\Teste\\Gereciador de leituras\\Imagens\\book2-removebg-preview.png", width=200) #Imagem pra dar vida

    title_input = ft.TextField(label="Título", width=200)
    author_input = ft.TextField(label="Autor", width=200)
    total_pages_input = ft.TextField(label="Total de Páginas", keyboard_type=ft.KeyboardType.NUMBER, width=150)
    pages_read_input = ft.TextField(label="Última Página Lida", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    
    status_options = ["Em andamento", "Concluído", "Pausado", "Abandonado", "Planejado"]
    status_dropdown = ft.Dropdown(label="Status da Leitura", options=[ft.dropdown.Option(text=opt) for opt in status_options], width=200)
    
    book_list = ft.Column()

    def update_book_list():
        book_list.controls.clear()
        for book in books:
            remaining_pages = book['total_pages'] - book['pages_read']
            percentage = (book['pages_read'] / book['total_pages']) * 100 if book['total_pages'] > 0 else 0
            update_pages_input = ft.TextField(label="Última página lida", width=150, keyboard_type=ft.KeyboardType.NUMBER)
            
            book_list.controls.append(
                ft.Row([
                    update_pages_input,
                    ft.ElevatedButton("Atualizar", on_click=lambda e, b=book, inp=update_pages_input: update_progress(b, inp)),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, b=book: delete_book(b)),
                    ft.Column([
                        ft.Text(f"{book['title']} - {book['author']} ({percentage:.2f}%) - Faltam {remaining_pages} páginas - Status: {book['status']}")
                    ], expand=True)
                ], alignment=ft.MainAxisAlignment.START)
            )
        page.update()
    
    def add_book(e):
        if title_input.value and author_input.value and total_pages_input.value.isdigit():
            new_book = {
                "title": title_input.value,
                "author": author_input.value,
                "total_pages": int(total_pages_input.value),
                "pages_read": int(pages_read_input.value) if pages_read_input.value.isdigit() else 0,
                "status": status_dropdown.value if status_dropdown.value else "Em andamento"
            }
            books.append(new_book)
            save_books(books)
            update_book_list()
            title_input.value = ""
            author_input.value = ""
            total_pages_input.value = ""
            pages_read_input.value = ""
            status_dropdown.value = ""
            page.update()
    
    def delete_book(book):
        books.remove(book)
        save_books(books)
        update_book_list()
    
    def update_progress(book, input_field):
        if input_field.value.isdigit():
            new_page = int(input_field.value)
            book['pages_read'] = new_page
            if book['pages_read'] > book['total_pages']:
                book['pages_read'] = book['total_pages']
            save_books(books)
            update_book_list()
            input_field.value = ""
            page.update()
    
    update_book_list()
    
    page.add(
        ft.Row([theme_switch], alignment=ft.MainAxisAlignment.END),  # Switch no canto direito
        image, 
        ft.Row([title_input, author_input, total_pages_input, pages_read_input], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Row([status_dropdown], alignment=ft.MainAxisAlignment.CENTER),
        ft.ElevatedButton("Adicionar Livro", on_click=add_book),
        book_list
    )

ft.app(target=main)
