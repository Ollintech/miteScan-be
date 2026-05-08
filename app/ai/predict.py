import torch
from PIL import Image
from torchvision import transforms
from app.ai.model.cnn import MiteScanCNN

classes = ["normal", "varroa", "deformada"]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

model = MiteScanCNN()

# força criação da fc1
dummy_input = torch.randn(1, 3, 224, 224)
model(dummy_input)

model.load_state_dict(torch.load("app/ai/model/best_model.pth"))
model.eval()


def predict_image(image_path):

    img = Image.open(image_path).convert("RGB")
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(img)
        probs = torch.softmax(output, dim=1)

        classe_idx = torch.argmax(probs).item()
        confianca = probs[0][classe_idx].item()

    return {
        "classe": classes[classe_idx],
        "confianca": round(confianca, 2),
        "probabilidades": {
            classes[i]: round(prob.item(), 2)
            for i, prob in enumerate(probs[0])
        }
    }