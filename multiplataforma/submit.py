import roboflow

rf = roboflow.Roboflow()
workspace = rf.workspace("evtol-ita-3dksr")
dataset = workspace.upload_dataset(
    "./batch2",  # Caminho para o seu conjunto de dados
    project_name="sae_comeback",
    dataset_format="yolov8",  # Formato das anotações
    project_license="MIT",  # Licença do projeto
    project_type="object-detection"  # Tipo de projeto
)
