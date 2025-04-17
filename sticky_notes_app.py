import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, font
import os
import json # Adicionar import para JSON

# --- Definições de Temas ---
THEMES = {
    "light": {
        "bg": "#F5F5F5",
        "fg": "#000000",
        "list_bg": "#FFFFFF",
        "list_fg": "#000000",
        "list_select_bg": "#D3D3D3",
        "text_bg": "#FFFFFF",
        "text_fg": "#000000",
        "button_bg": "#E0E0E0",
        "button_fg": "#000000",
        "button_active_bg": "#C8C8C8",
    },
    "dark": {
        "bg": "#2E2E2E",
        "fg": "#FFFFFF",
        "list_bg": "#3C3C3C",
        "list_fg": "#FFFFFF",
        "list_select_bg": "#505050",
        "text_bg": "#3C3C3C",
        "text_fg": "#FFFFFF",
        "button_bg": "#505050",
        "button_fg": "#FFFFFF",
        "button_active_bg": "#646464",
    }
}

NOTE_SEPARATOR = "\n---END_NOTE---\n" # Usar \n para garantir que funcione em diferentes SOs
CONFIG_FILE = "config.json" # Nome do arquivo de configuração

class StickyNotesApp:
    def __init__(self, master):
        self.master = master
        master.title("Notas Autoadesivas - INSS")
        master.geometry("700x450") # Tamanho inicial ajustado

        # --- Definir Ícone ---
        try:
            # Certifique-se que 'icon.png' está no mesmo diretório
            icon_path = "icon.png"
            if os.path.exists(icon_path):
                 # O primeiro argumento 'False' indica que é a janela principal
                 # Usamos PhotoImage para PNG, GIF. Para .ico, use master.iconbitmap(icon_path)
                img = tk.PhotoImage(file=icon_path)
                master.iconphoto(False, img)
            else:
                print(f"Aviso: Arquivo de ícone '{icon_path}' não encontrado.")
        except tk.TclError as e:
            print(f"Erro ao carregar ícone '{icon_path}': {e}. Certifique-se que é um formato válido (PNG, GIF).")
        except Exception as e:
             print(f"Erro inesperado ao definir ícone: {e}")

        # --- Lógica de Dados e Configuração ---
        self.notes_file = "notes.txt"
        self.notes_data = [] # Lista de dicionários {'title': str, 'content': str}
        self.current_selected_index = None
        self.config_file = CONFIG_FILE
        self.current_theme = "light" # Padrão inicial antes de carregar config
        self.note_font = font.Font(family="Arial", size=10) # Fonte padrão para Listbox e Text

        # --- Carregar Configurações (inclusive o tema) ---
        self.load_config()

        # --- Configurar Layout Principal (PanedWindow) ---
        # Usar PanedWindow para permitir redimensionamento
        self.paned_window = tk.PanedWindow(master, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Painel Esquerdo (Lista de Notas) ---
        self.list_frame = tk.Frame(self.paned_window, width=200) # Largura inicial sugerida
        self.paned_window.add(self.list_frame, stretch="never") # Não esticar inicialmente
        self.list_frame.rowconfigure(1, weight=1) # Listbox expande verticalmente
        self.list_frame.columnconfigure(0, weight=1) # Coluna principal expande horizontalmente

        # Botão de Tema (movido para o topo para melhor acesso)
        self.theme_button = tk.Button(self.list_frame, text="🌙", width=3, command=self.toggle_theme)
        self.theme_button.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))

        # Título da Lista
        self.list_label = tk.Label(self.list_frame, text="Notas", font=('Arial', 12, 'bold'))
        self.list_label.grid(row=0, column=0, sticky="s", pady=(5, 10)) # Centralizado na parte inferior da linha 0

        # Listbox
        self.notes_listbox = tk.Listbox(self.list_frame, selectmode=tk.SINGLE, exportselection=False, font=self.note_font, borderwidth=0, highlightthickness=0)
        self.notes_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=(0,5))
        self.notes_listbox.bind('<<ListboxSelect>>', self.display_selected_note)

        # Botões Add/Delete em um frame próprio para melhor layout
        button_frame = tk.Frame(self.list_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 5))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.add_button = tk.Button(button_frame, text="+ Adicionar", command=self.add_note)
        self.add_button.grid(row=0, column=0, sticky="ew", padx=(0, 2))

        self.delete_button = tk.Button(button_frame, text="- Excluir", command=self.delete_note)
        self.delete_button.grid(row=0, column=1, sticky="ew", padx=(2, 0))

        # --- Painel Direito (Conteúdo da Nota) ---
        self.content_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.content_frame, stretch="always") # Este painel estica
        self.content_frame.rowconfigure(1, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        self.content_label = tk.Label(self.content_frame, text="Conteúdo", font=('Arial', 12, 'bold'))
        self.content_label.grid(row=0, column=0, pady=(10, 5)) # Ajuste no padding

        self.note_content_text = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, state=tk.DISABLED, font=self.note_font, borderwidth=0, highlightthickness=0)
        self.note_content_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        # Bind para salvar automaticamente (ou com botão)
        self.note_content_text.bind("<KeyRelease>", self.mark_unsaved) # Marcar como não salvo ao digitar

        self.save_button = tk.Button(self.content_frame, text="Salvar Alterações", command=self.save_note_content, state=tk.DISABLED)
        self.save_button.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 5))

        # --- Carregar Dados e Aplicar Tema Inicial (agora baseado na config) ---
        self.load_notes()
        self.apply_theme() # Aplicar tema (pode ter sido carregado da config)

        # --- Salvar ao Fechar ---
        master.protocol("WM_DELETE_WINDOW", self.on_closing) # Salvar ao fechar

    # --- Métodos de Configuração ---
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    # Garante que o tema carregado seja válido
                    self.current_theme = config_data.get("theme", "light") if config_data.get("theme") in THEMES else "light"
            else:
                # Se o arquivo não existe, usa o padrão e salva pela primeira vez
                self.save_config()
        except (json.JSONDecodeError, IOError, Exception) as e:
            print(f"Erro ao carregar configuração de '{self.config_file}': {e}. Usando tema padrão.")
            self.current_theme = "light" # Volta ao padrão em caso de erro

    def save_config(self):
        config_data = {
            "theme": self.current_theme
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4) # Salva com indentação para legibilidade
        except (IOError, Exception) as e:
             print(f"Erro ao salvar configuração em '{self.config_file}': {e}")

    # --- Métodos de Tema ---
    def apply_theme(self):
        theme = THEMES[self.current_theme]
        colors = theme # Alias para clareza

        # Janela Principal
        self.master.config(bg=colors["bg"])

        # PanedWindow Sash (pode não ser diretamente configurável via cores padrão)
        # Tentativa de configurar os frames internos
        self.list_frame.config(bg=colors["list_bg"])
        self.content_frame.config(bg=colors["bg"])

        # Elementos do List Frame
        self.list_label.config(bg=colors["list_bg"], fg=colors["fg"])
        self.notes_listbox.config(
            bg=colors["list_bg"], fg=colors["list_fg"],
            selectbackground=colors["list_select_bg"], selectforeground=colors["list_fg"]
        )
        # Botão de tema (ícone pode precisar de ajuste manual)
        theme_icon = "☀️" if self.current_theme == "dark" else "🌙"
        self.theme_button.config(
             text=theme_icon,
             bg=colors["button_bg"], fg=colors["button_fg"],
             activebackground=colors["button_active_bg"], activeforeground=colors["button_fg"],
             borderwidth=0, highlightthickness=0
        )
        # Frame dos botões add/delete
        # Acessar o frame de botões de forma mais robusta (assumindo que é o último widget adicionado ao list_frame)
        button_frame_widget = self.list_frame.winfo_children()[-1]
        if isinstance(button_frame_widget, tk.Frame):
            button_frame_widget.config(bg=colors["list_bg"])

        # Botões Add/Delete
        self.add_button.config(bg=colors["button_bg"], fg=colors["button_fg"], activebackground=colors["button_active_bg"], activeforeground=colors["button_fg"], borderwidth=0, highlightthickness=0)
        self.delete_button.config(bg=colors["button_bg"], fg=colors["button_fg"], activebackground=colors["button_active_bg"], activeforeground=colors["button_fg"], borderwidth=0, highlightthickness=0)


        # Elementos do Content Frame
        self.content_label.config(bg=colors["bg"], fg=colors["fg"])
        self.note_content_text.config(
            bg=colors["text_bg"], fg=colors["text_fg"],
            insertbackground=colors["text_fg"] # Cor do cursor
        )
        self.save_button.config(bg=colors["button_bg"], fg=colors["button_fg"], activebackground=colors["button_active_bg"], activeforeground=colors["button_fg"], borderwidth=0, highlightthickness=0, disabledforeground=THEMES['light' if self.current_theme == 'dark' else 'dark']["list_select_bg"]) # Cor quando desabilitado

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        self.save_config() # Salva a nova preferência de tema

    def mark_unsaved(self, event=None):
        if self.current_selected_index is not None:
            self.save_button.config(state=tk.NORMAL, text="Salvar Alterações*")

    def load_notes(self):
        self.notes_data = []
        self.notes_listbox.delete(0, tk.END) # Limpar listbox
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    raw_notes = content.split(NOTE_SEPARATOR)
                    for note_block in raw_notes:
                        if note_block.strip(): # Ignorar blocos vazios (ex: após o último separador)
                            parts = note_block.strip().split('\n', 1) # Usar \n como no save
                            title = parts[0]
                            note_content = parts[1] if len(parts) > 1 else ""
                            self.notes_data.append({"title": title, "content": note_content})
                            self.notes_listbox.insert(tk.END, title)
            except Exception as e:
                messagebox.showerror("Erro ao Carregar", f"Não foi possível ler o arquivo de notas: {e}")
        # Selecionar a primeira nota se houver alguma
        if self.notes_data:
             self.notes_listbox.select_set(0)
             self.notes_listbox.event_generate("<<ListboxSelect>>")
        else:
             self.clear_content_area() # Limpar se não houver notas

    def save_notes_to_file(self):
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                notes_to_write = []
                for note in self.notes_data:
                    # Garante que o título não tenha novas linhas internas acidentais
                    # O conteúdo pode ter novas linhas, que são preservadas
                    title = note.get('title', 'Sem Título').replace('\n', ' ')
                    content = note.get('content', '')
                    notes_to_write.append(f"{title}\n{content}") # Usar \n literal para o split
                f.write(NOTE_SEPARATOR.join(notes_to_write))
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar as notas no arquivo: {e}")

    def display_selected_note(self, event=None):
        selected_indices = self.notes_listbox.curselection()
        if not selected_indices:
            self.current_selected_index = None
            self.clear_content_area()
            return

        self.current_selected_index = selected_indices[0]
        note_data = self.notes_data[self.current_selected_index]

        self.note_content_text.config(state=tk.NORMAL)
        self.note_content_text.delete('1.0', tk.END)
        self.note_content_text.insert('1.0', note_data.get('content', ''))
        self.save_button.config(state=tk.DISABLED, text="Salvar Alterações") # Resetar botão save

    def clear_content_area(self):
         self.note_content_text.delete('1.0', tk.END)
         self.note_content_text.config(state=tk.DISABLED)
         self.save_button.config(state=tk.DISABLED, text="Salvar Alterações")
         self.current_selected_index = None


    def add_note(self):
        note_title = simpledialog.askstring("Nova Nota", "Digite o título da nova nota:", parent=self.master)
        if note_title: # Se o usuário não cancelou
            note_title = note_title.strip()
            if not note_title: # Se digitou apenas espaços
                note_title = "Nova Nota Sem Título"

            # Verificar se título já existe (opcional, mas bom)
            # if any(note['title'] == note_title for note in self.notes_data):
            #     messagebox.showwarning("Título Duplicado", "Já existe uma nota com este título.")
            #     return

            new_note = {"title": note_title, "content": ""}
            self.notes_data.append(new_note)
            self.notes_listbox.insert(tk.END, note_title)
            self.notes_listbox.selection_clear(0, tk.END)
            self.notes_listbox.selection_set(tk.END) # Seleciona a nova nota
            self.notes_listbox.see(tk.END) # Garante que a nova nota esteja visível
            self.notes_listbox.event_generate("<<ListboxSelect>>") # Dispara o evento para exibir
            self.note_content_text.focus_set() # Foca na área de texto para edição
            self.save_notes_to_file() # Salva imediatamente a criação da nota

    def delete_note(self):
        if self.current_selected_index is None:
            messagebox.showwarning("Nenhuma Nota Selecionada", "Selecione uma nota para excluir.")
            return

        note_title = self.notes_data[self.current_selected_index]['title']
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a nota '{note_title}'?", parent=self.master):
            del self.notes_data[self.current_selected_index]
            self.notes_listbox.delete(self.current_selected_index)
            self.save_notes_to_file()

            # Limpar a área de conteúdo ou selecionar a próxima/anterior nota
            if self.notes_data:
                new_index = max(0, self.current_selected_index - 1) if self.current_selected_index > 0 else 0
                if new_index < self.notes_listbox.size():
                     self.notes_listbox.selection_set(new_index)
                     self.notes_listbox.event_generate("<<ListboxSelect>>")
                else: # Se excluiu a última
                    self.clear_content_area()

            else: # Se não há mais notas
                self.clear_content_area()


    def save_note_content(self):
        if self.current_selected_index is None:
            # Isso não deveria acontecer se o botão está habilitado, mas por segurança
            messagebox.showwarning("Erro", "Nenhuma nota selecionada para salvar.")
            return

        current_content = self.note_content_text.get("1.0", tk.END).strip()
        self.notes_data[self.current_selected_index]['content'] = current_content
        self.save_notes_to_file()
        self.save_button.config(state=tk.DISABLED, text="Salvar Alterações") # Desabilitar após salvar
        # Opcional: Atualizar título se a primeira linha mudou? Por enquanto não.

    def on_closing(self):
        # Verificar se há alterações não salvas na nota atual
        if self.save_button['state'] == tk.NORMAL:
             if messagebox.askyesno("Sair", "Você tem alterações não salvas. Deseja salvá-las antes de sair?", parent=self.master):
                 self.save_note_content() # Salva a nota atual
             # Se clicar não, simplesmente fecha sem salvar a última edição

        # Não é necessário chamar save_notes_to_file() aqui novamente
        # pois add/delete/save_note_content já salvam o estado geral.
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StickyNotesApp(root)
    root.mainloop() 