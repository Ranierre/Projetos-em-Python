import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from audio_preprocessor import convert_mp3_to_wav, load_audio
from melody_extractor import extract_melody
from chord_recognizer import extract_chords
from score_generator import creat_score


class AudioAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador Musical")
        self.root.geometry("600x400")

        self.creat_widgets()

    def creat_widgets(self):
        #frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Seção de seleção de arquivos
        file_frame = ttk.LabelFrame(main_frame, text="Arquivo de Áudio", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Procurar", command=self.browse_file).pack(side=tk.LEFT)
        #Seletor de Opções
        options_frame = ttk.LabelFrame(main_frame, text="Opções", padding="10")
        options_frame.pack(fill=tk.X, pady=5)

        self.extract_melody = tk.BooleanVar(value=True)
        self.extract_chords = tk.BooleanVar(value=True)
        self.generate_score = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Extrair Melodia", variable=self.extract_melody).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Extrair Acordes", variable=self.extract_chords).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Gerar Partitura", variable=self.generate_score).pack(anchor=tk.W)

        # Botão de processamento:
        ttk.Button(main_frame, text="Processar Áudio", command=self.process_audio).pack(pady=10)

        # Areas de resultados
        self.result_text = tk.Text(main_frame, height=10, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        #Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)

    def browse_file(self):
        filetypes = (
            ('Arquivos MP3', '*.mp3'),
            ('Todos os Arquivos', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Selecione um arquivo de áudio',
            initialdir='/',
            filetypes=filetypes
        )
        if filename:
            self.file_path.set(filename)

    def process_audio(self):
        if not self.file_path.get():
            messagebox.showerror("Erro", "Selecione um arquivo de audio primeiro")
            return
        try:
            #Atualizar interface:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Processando...\n")
            self.root.update()
            #1. pre - processamento
            self.progress['value'] = 20
            wav_file = os.path.splitext(self.file_path.get())[0] + ".wav"
            convert_mp3_to_wav(self.file_path.get(), wav_file)
            signal, sr = load_audio(wav_file)

            #2. Extrair Melodia
            if self.extract_melody.get():
                self.progress['value'] = 40
                melody_notes = extract_melody(signal, sr)
                self.result_text.insert(tk.END, f"\nMelodia Detectada ({len(melody_notes)} notas):\n")
                self.result_text.insert(tk.END, ",".join(melody_notes[:20]) + "...\n")

            #Extração dos acordes
            if self.extract_chords.get():
                self.progress['value'] = 60
                chords = extract_chords(signal, sr)
                self.result_text.insert(tk.END, "\nAcordes Detectados:\n")

                for time, chord_name in chords[:10]: #Mostra os 10 primeiros (devemos aumentar futuramente)
                    self.result_text.insert(tk.END, f"{time:.1f}s: {chord_name}\n")

            # 4 Gerar uma partitura
            if self.generate_score.get() and self.extract_melody.get():
                self.progress['value'] = 80
                output_pdf = os.path.splitext(self.file_path.get())[0] + "_partitura.pdf"
                creat_score(melody_notes, output_pdf=output_pdf)
                self.result_text.insert(tk.END, f"\nPartitura gerada com sucesso em: {output_pdf}\n")
            self.progress['value'] = 100
            messagebox.showinfo("Sucesso", "Processamento Conclúido")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro, tente novamente:\n{str(e)}")
            self.progress['value'] = 0

def main():
    root = tk.Tk()
    app = AudioAnalyzerApp(root)
    root.mainloop()

if __name__=="__main__":
    main()