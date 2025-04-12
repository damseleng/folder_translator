import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import deepl
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("フォルダ名翻訳ツール")
        self.root.geometry("800x600")
        
        self.selected_path = tk.StringVar()
        self.api_key = tk.StringVar()
        self.translator = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # フォルダ選択部分
        folder_frame = ttk.Frame(self.root)
        folder_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(folder_frame, text="フォルダ選択", command=self.select_folder).pack(side='left')
        ttk.Label(folder_frame, textvariable=self.selected_path).pack(side='left', padx=5)
        
        # API Key入力部分
        api_frame = ttk.Frame(self.root)
        api_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(api_frame, text="DeepL API Key:").pack(side='left')
        ttk.Entry(api_frame, textvariable=self.api_key, width=50).pack(side='left', padx=5)
        
        # プログレスバー
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.pack(fill='x', padx=5, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_label = ttk.Label(self.progress_frame, text="")
        self.progress_label.pack(side='top', pady=2)
        self.progress.pack(fill='x', pady=2)
        
        # プレビュー領域
        preview_frame = ttk.Frame(self.root)
        preview_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('original', 'translated')
        self.preview_tree = ttk.Treeview(preview_frame, columns=columns, show='headings')
        
        self.preview_tree.heading('original', text='元の名前')
        self.preview_tree.heading('translated', text='翻訳後の名前')
        
        self.preview_tree.column('original', width=350)
        self.preview_tree.column('translated', width=350)
        
        scrollbar = ttk.Scrollbar(preview_frame, orient='vertical', command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        self.preview_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 実行ボタン
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="実行", command=self.execute_rename).pack(side='right', padx=5)
        ttk.Button(button_frame, text="プレビュー", command=self.translate_and_preview).pack(side='right', padx=5)
    
    def update_progress(self, value, text):
        self.progress_var.set(value)
        self.progress_label.config(text=text)
        self.root.update_idletasks()
    
    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_path.set(folder_path)
            self.preview_tree.delete(*self.preview_tree.get_children())
    
    def translate_and_preview(self):
        if not self.selected_path.get():
            messagebox.showerror("エラー", "フォルダを選択してください。")
            return
        
        if not self.api_key.get():
            messagebox.showerror("エラー", "DeepL API Keyを入力してください。")
            return
        
        try:
            self.translator = deepl.Translator(self.api_key.get())
            self.preview_tree.delete(*self.preview_tree.get_children())
            
            folder_path = Path(self.selected_path.get())
            items = list(folder_path.glob('*'))
            total_items = len(items)
            
            self.update_progress(0, "翻訳を開始します...")
            
            for i, item in enumerate(items, 1):
                original_name = item.name
                try:
                    self.update_progress(i / total_items * 100, f"翻訳中: {original_name}")
                    result = self.translator.translate_text(original_name, target_lang="JA")
                    translated_name = result.text
                    self.preview_tree.insert('', 'end', values=(original_name, translated_name))
                except Exception as e:
                    messagebox.showerror("翻訳エラー", f"'{original_name}'の翻訳中にエラーが発生しました: {str(e)}")
            
            self.update_progress(100, "翻訳が完了しました")
                    
        except Exception as e:
            messagebox.showerror("エラー", f"APIの初期化に失敗しました: {str(e)}")
            self.update_progress(0, "エラーが発生しました")
    
    def execute_rename(self):
        if not self.preview_tree.get_children():
            messagebox.showerror("エラー", "プレビューを実行してください。")
            return
        
        if not messagebox.askyesno("確認", "選択したフォルダ内のアイテムの名前を変更します。よろしいですか？"):
            return
        
        folder_path = Path(self.selected_path.get())
        errors = []
        items = self.preview_tree.get_children()
        total_items = len(items)
        
        self.update_progress(0, "名前変更を開始します...")
        
        for i, item in enumerate(items, 1):
            values = self.preview_tree.item(item)['values']
            original_name = values[0]
            translated_name = values[1]
            
            try:
                self.update_progress(i / total_items * 100, f"名前変更中: {original_name} → {translated_name}")
                original_path = folder_path / original_name
                new_path = folder_path / translated_name
                original_path.rename(new_path)
            except Exception as e:
                errors.append(f"'{original_name}'の名前変更に失敗しました: {str(e)}")
        
        if errors:
            messagebox.showerror("エラー", "\n".join(errors))
            self.update_progress(0, "エラーが発生しました")
        else:
            messagebox.showinfo("完了", "名前の変更が完了しました。")
            self.preview_tree.delete(*self.preview_tree.get_children())
            self.selected_path.set("")
            self.update_progress(100, "処理が完了しました")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()