import replicate


class EmbeddingModel:

    def __init__(self):
        pass

    def embed_image(self, image_url: str):
        embedding = replicate.run(
            "daanelson/imagebind:0383f62e173dc821ec52663ed22a076d9c970549c209666ac3db181618b7a304",
            input={"input": image_url, "modality": "vision"},
        )

        return embedding

    def embed_text(self, text: str):
        embedding = replicate.run(
                "daanelson/imagebind:0383f62e173dc821ec52663ed22a076d9c970549c209666ac3db181618b7a304",
                input={"text_input": text, "modality": "text"},
            )
        return embedding
    
    def generate_description(self, image_url: str):
        description = replicate.run(
            "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
            input={
                "task": "image_captioning",
                "image": image_url,
            },
        )
        # Remove the "Caption: " prefix if it exists
        if len(description) >= 9 and description[:9] == "Caption: ":
            description = description[9:]
        
        return description