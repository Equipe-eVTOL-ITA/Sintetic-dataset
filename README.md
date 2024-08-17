# Criação de dataset sintético da arena

(Rascunho)

**Arena.blender**: Arena modelada em Blender. Para que os papéis de parede sejam adicionados, os arquivos .png "Fundo", "Parede_1" e "Parede_2" devem estar no mesmo diretório do .blender

**Blender.py**: contém classes (e métodos) úteis à criação do *dataset*, em particular definidas para os sistemas de referência dentre quais as transformadas ocorrem (câmera e imagem).

**Dataset.py**: implementa efetivamente a criação do *dataset* a partir do Blender.

## Exemplos de *dataset* criado

![img_23](https://github.com/user-attachments/assets/9c99b88f-7823-41bc-bf84-46a970010862)
![img_16](https://github.com/user-attachments/assets/97aebd85-2b5b-4450-b8b4-6484d28f575d)

## Exemplos de *labels* associadas às imagens

![train_2](https://github.com/user-attachments/assets/8a2a3ea0-d1ce-43c5-bf1d-1baa2dbda4df)
![train_8](https://github.com/user-attachments/assets/147109ce-2407-4b11-b2df-b9f3eae3fc5a)
![train_5](https://github.com/user-attachments/assets/2859d676-c6dc-4e97-83c1-7d3f91ed2f26)
