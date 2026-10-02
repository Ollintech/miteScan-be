import os
import torch
from PIL import Image
from torchvision import transforms
from ai.model.cnn import MiteScanCNN

classes = ["normal", "varroa", "deformada"]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

model = MiteScanCNN()

# força criação da fc1
dummy_input = torch.randn(1, 3, 224, 224)
model(dummy_input)

# 🔄 CORREÇÃO AQUI: Caminho dinâmico e seguro para o model.pth
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "model", "best_model.pth")

model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()


def predict_image(image_path):

    img = Image.open(image_path).convert("RGB")
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(img)
        probs = torch.softmax(output, dim=1)

        classe_idx = int(torch.argmax(probs).item())
        confianca = float(probs[0][classe_idx].item())

    return {
        "classe": classes[classe_idx],
        "confianca": round(confianca, 2),
        "probabilidades": {
            classes[i]: round(float(prob.item()), 2)
            for i, prob in enumerate(probs[0])
        }
    }