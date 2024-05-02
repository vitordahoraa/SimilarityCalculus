import utils
import pandas as pd
import utils as util
import tkinter as tk
'''
Dataset = utils.readDataset()

Weights = utils.readWeights()

MaxValues, MinValues = util.getMaxAndMin(Dataset)

WeightsSum = util.sumWeights(Weights)

Inputs = util.readInput()

Outputs = util.calcSimilarity(Inputs,Dataset,Weights,WeightsSum,MaxValues,MinValues,'')

util.writeOutput(Outputs)
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class InterfaceGrafica:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("RCB")
        self.Weights = util.readWeights()
        self.df = 'Carregue um dataset primeiro' #util.readDataset()[1:100]

        # Criar o widget de notebook para as abas
        self.abas = ttk.Notebook(self.janela)

        scroll_bar = tk.Scrollbar(self.janela)

        # Aba de entrada de texto
        self.aba_pesos = ttk.Frame(self.abas)
        self.abas.add(self.aba_pesos, text="Pesos")
        self.criar_aba_pesos()

        # Aba de exibição de DataFrame
        self.aba_dataframe = ttk.Frame(self.abas)
        self.abas.add(self.aba_dataframe, text="DataFrame")
        self.criar_aba_dataframe()

        # Aba de input de casos
        self.aba_input = ttk.Frame(self.abas)
        self.abas.add(self.aba_input, text="Input")
        self.criar_aba_input()

        # Aba de output de casos
        self.aba_output = ttk.Frame(self.abas)
        self.abas.add(self.aba_output, text="Output")
        self.criar_aba_output()


        # Exibir as abas
        self.abas.pack(expand=True, fill="both")

    def criar_aba_pesos(self):
        # Criar os widgets para entrada de peso
        self.labelWeight = {}
        self.textWeight = {}

        print(self.Weights)
        counter = 0

        for columnName in self.Weights:
            self.labelWeight[columnName] = tk.Label(self.aba_pesos, text=columnName)
            self.labelWeight[columnName].grid(row=counter, column=0, padx=5, pady=5)
            initWeight = tk.StringVar()
            initWeight.set(self.Weights[columnName].iloc[0])
            self.textWeight[columnName] = tk.Entry(self.aba_pesos, textvariable=initWeight)
            self.textWeight[columnName].grid(row=counter, column=1, padx=5, pady=5)
            counter = counter + 1



        # Botão para exibir os textos
        self.botao_exibir_weight = tk.Button(self.aba_pesos, text="Atualizar Pesos", command=self.atualizar_pesos)
        self.botao_exibir_weight.grid(row=counter, columnspan=2, padx=5, pady=5)

    def criar_aba_dataframe(self):
        # Criar um DataFrame simples
        '''dados = {'Nome': ['Alice', 'Bob', 'Charlie', 'David'],
                 'Idade': [25, 30, 35, 40],
                 'Cidade': ['A', 'B', 'C', 'D']}
        self.df = pd.DataFrame(dados)
        '''

        # Exibir o DataFrame em uma caixa de texto
        self.texto_dataframe = tk.Text(self.aba_dataframe, height=40, width=220, wrap='none')
        if(isinstance(self.df,str)):
            print(self.df)
            self.texto_dataframe.insert(tk.END, self.df)
        else:
            self.texto_dataframe.insert(tk.END, self.df.to_string(index=False))
        # Botão para incluir input

        self.texto_dataframe.config(state=tk.DISABLED)
        self.texto_dataframe.pack(padx=10, pady=10)

        self.botao_refresh_dataframe = tk.Button(self.aba_dataframe, text="Refresh", command=self.refresh_output)
        self.botao_refresh_dataframe.pack(padx=10, pady=10)


    def refresh_output(self):
        self.aba_dataframe.destroy()
        self.aba_dataframe = ttk.Frame(self.abas)
        self.abas.add(self.aba_dataframe, text="DataFrame")
        self.criar_aba_dataframe()

    def atualizar_pesos(self):
        for columnName in self.Weights:
            # Obter os textos inseridos e exibir em uma caixa de mensagem
            self.Weights[columnName] = self.textWeight[columnName].get()
        utils.writeWeights(self.Weights)
        mensagem = f"Pesos Atualizados com sucesso"
        messagebox.showinfo("Pesos Atualizados com sucesso", mensagem)
    def criar_aba_input(self):

        self.labelInputCase = tk.Label(self.aba_input, text="Case")
        self.labelInputCase.grid(row=0, column=0, padx=5, pady=5)
        initInputCase = tk.StringVar()
        initInputCase.set("Caso1")
        self.textInputCase = tk.Entry(self.aba_input, textvariable=initInputCase)
        self.textInputCase.grid(row=0, column=1, padx=5, pady=5)



        self.labelInputEntity = tk.Label(self.aba_input, text="Entity")
        self.labelInputEntity.grid(row=1, column=0, padx=5, pady=5)
        initInputEntity = tk.StringVar()
        initInputEntity.set("Brazil")
        self.textInputEntity = tk.Entry(self.aba_input, textvariable=initInputEntity)
        self.textInputEntity.grid(row=1, column=1, padx=5, pady=5)

        self.labelInputWeek = tk.Label(self.aba_input, text="Week")
        self.labelInputWeek.grid(row=2, column=0, padx=5, pady=5)
        initInputWeek = tk.StringVar()
        initInputWeek.set("15")
        self.textInputWeek = tk.Entry(self.aba_input, textvariable=initInputWeek)
        self.textInputWeek.grid(row=2, column=1, padx=5, pady=5)

        self.labelInputArea = tk.Label(self.aba_input, text="area burnt by wildfires in 2024")
        self.labelInputArea.grid(row=3, column=0, padx=5, pady=5)
        initInputArea = tk.StringVar()
        initInputArea.set("6122")
        self.textInputArea = tk.Entry(self.aba_input, textvariable=initInputArea)
        self.textInputArea.grid(row=3, column=1, padx=5, pady=5)

        # Botão para incluir input
        self.botao_exibir_input = tk.Button(self.aba_input, text="Inserir caso", command=self.escrever_input)
        self.botao_exibir_input.grid(row=4, columnspan=2, padx=5, pady=5)



    def escrever_input(self):
        # Criar um DataFrame simples
        Input = {'Entity': [self.textInputEntity.get()],
                 'Week': [self.textInputWeek.get()],
                 'area burnt by wildfires in 2024': [self.textInputArea.get()]
                 }
        Input = pd.DataFrame(Input)

        utils.writeInput(Input, self.textInputCase.get())

        mensagem = f"Input {self.textInputCase.get()} Inserido com sucesso"
        messagebox.showinfo("Input Inserido com sucesso", mensagem)

    def criar_aba_output(self):

        # Botão para incluir input
        self.botao_exibir_output = tk.Button(self.aba_output, text="Atualizar Similaridades", command=self.escrever_output)
        self.botao_exibir_output.grid(row=0, columnspan=2, padx=5, pady=5)


        self.labelOutputCase = tk.Label(self.aba_output, text="Case")
        self.labelOutputCase.grid(row=1, column=0, padx=5, pady=5)
        initOutputCase = tk.StringVar()
        initOutputCase.set("Caso1")
        self.textOutputCase = tk.Entry(self.aba_output, textvariable=initOutputCase)
        self.textOutputCase.grid(row=1, column=1, padx=5, pady=5)


    def escrever_output(self):

        Inputs = util.readInput()
        Dataset = util.readDataset()
        WeightsSum = util.sumWeights(self.Weights)
        MaxValue, MinValue = util.getMaxAndMin(Dataset)

        Output = util.calcSimilarity(Inputs,Dataset,self.Weights,WeightsSum,MaxValue,MinValue,self.textOutputCase.get())

        self.df = Output[self.textOutputCase.get()].copy().sort_values('Similarity',ascending=False)

        util.writeOutput(Output)

        mensagem = f"Output {self.textOutputCase.get()} gerado com sucesso"
        messagebox.showinfo("Output Inserido com sucesso", mensagem)





# Criar a janela principal
janela = tk.Tk()
app = InterfaceGrafica(janela)
janela.mainloop()
