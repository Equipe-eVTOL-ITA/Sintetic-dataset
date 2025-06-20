import roboflow
import argparse

parser = argparse.ArgumentParser()

# batch number
parser.add_argument('--b', type=int, required=True)
args = parser.parse_args()

rf = roboflow.Roboflow()
workspace = rf.workspace("evtol-ita-3dksr")
dataset = workspace.upload_dataset(
    f"./batch{args.b}",  # Caminho para o seu conjunto de dados
    project_name="the_last_dance",
    dataset_format="yolov8",  # Formato das anotações
    project_license="MIT",  # Licença do projeto
    project_type="object-detection"  # Tipo de projeto
)
